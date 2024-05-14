# Project     : kraken2df
# File Name   : genus_report.py
# Description : Genus level report object and methods.
# Author      : Todd N. Wylie
# Email       : twylie@wustl.edu
# Created     : Mon May 13 12:36:51 CDT 2024
# Copyright   : Copyright (C) 2024 by T.N. Wylie. All rights reserved.

import pandas as pd  # type: ignore
from pathlib import Path
from typing import Self


class GenusReport():
    """Genus level report object and methods."""

    def __init__(self: Self) -> None:
        """Construct the class."""
        self.df: pd.core.frame.DataFrame
        self.df_f: pd.core.frame.DataFrame
        return

    def collect_counts(
            self: Self,
            df: pd.core.frame.DataFrame
            ) -> pd.core.frame.DataFrame:
        """Collect and separate the family read counts."""
        # APPROACH:
        # 1. Group by domain, kingdom, and phylum, class, order,
        # family, and genus.
        # 2. Get the first row of the groups.
        # 3. If (1) genus is not undef and (2) downstream fields are
        # all undef, use the counts for the genus level counts.
        # 4. ... else ignore and move on.
        # 5. From the original, full dataframe, remove the rows used for
        # counts based on index id. As we move to the next level, the
        # count-rows used here are no longer needed.
        drop_cols = ['species']
        dfg = df.groupby([
            'domain',
            'kingdom',
            'phylum',
            'class',
            'order',
            'family',
            'genus'
            ])
        df_i = dfg.head(1)
        df_i = df_i.copy()
        df_i = df_i.loc[
            (df_i['genus'] != 'undef') &
            (df_i['species'] == 'undef')
        ]
        remove_ids = df_i.index
        df_i = self.reset_sort(df=df_i)
        df_i.drop(drop_cols, axis=1, inplace=True)
        self.df = df_i.copy()
        df_revised = df.copy()
        df_revised.drop(index=remove_ids, inplace=True)
        return df_revised

    def format_report(
            self: Self,
            undef: bool = True,
            zeros: bool = True
            ) -> None:
        """Populates a formatted dataframe for a report."""
        df = self.df.copy()
        if undef is False:
            df = df.loc[df['genus'] != 'undef']
        if zeros is False:
            df = df.loc[df['counts'] > 0]
        df.reset_index(drop=True, inplace=True)
        self.df_f = df.copy()
        return

    def calc_total_reads(self: Self) -> int:
        """Calculate the total read count for a report."""
        counts = int(self.df['counts'].sum().item())
        return counts

    def calc_total_reads_formatted(self: Self) -> int:
        """Calculate the total read count for a formatted report."""
        counts = int(self.df_f['counts'].sum().item())
        return counts

    def save_report(
            self: Self,
            outdir: str,
            id: str,
            index: bool = True
            ) -> None:
        """Save a formatted report to a tab-delimited file."""
        counts = self.calc_total_reads_formatted()
        out_dir = Path(outdir)
        out_file = f'07.genus.{counts}.tsv'
        fho = out_dir / out_file
        df = self.df_f.copy()
        df.insert(0, 'sample_id', id)
        df['counts_pct'] = round(df['counts'].apply(lambda x: x / counts), 4)
        df.to_csv(fho, sep='\t', index=index)
        return

    def reset_sort(
            self: Self,
            df: pd.core.frame.DataFrame
            ) -> pd.core.frame.DataFrame:
        """Return a re-indexed and sorted genus report."""
        df = df.copy()
        df['counts'] = df['counts'].astype(int)
        df.sort_values(
            [
                'domain',
                'kingdom',
                'phylum',
                'class',
                'order',
                'family',
                'counts'
            ],
            ascending=[True, True, True, True, True, True, False],
            inplace=True
        )
        df.reset_index(inplace=True, drop=True)
        return df

    def append_to_counts(self: Self, family: pd.core.frame.DataFrame) -> None:
        """Append missing family read counts to genus report."""
        # APPROACH:
        # Some of the parent category entries may not be present at the
        # current (child) level; we need to add these entries to the
        # current, child report. We compare parent to child ids and
        # create rows for the missing entries at the child level,
        # labeling them as "undef" at the child level.
        df_f = family.copy()
        df_g = self.df.copy()
        df_f_ids = set(df_f.groupby(
            ['domain', 'kingdom', 'phylum', 'class', 'order', 'family']
        ).groups.keys())
        df_g_ids = set(df_g.groupby(
            ['domain', 'kingdom', 'phylum', 'class', 'order', 'family']
        ).groups.keys())
        missing_ids = df_f_ids.difference(df_g_ids)
        missing: dict = {
            'domain': [],
            'kingdom': [],
            'phylum': [],
            'class': [],
            'order': [],
            'family': [],
            'genus': [],
            'counts': []
        }
        dfg_f = df_f.groupby(
            ['domain', 'kingdom', 'phylum', 'class', 'order', 'family']
        )
        for id_ in missing_ids:
            domain, kingdom, phylum, class_, order, family = id_
            df = dfg_f.get_group(id_)
            counts = df['counts'].item()
            missing['domain'].append(domain)
            missing['kingdom'].append(kingdom)
            missing['phylum'].append(phylum)
            missing['class'].append(class_)
            missing['order'].append(order)
            missing['family'].append(family)
            missing['genus'].append('undef')
            missing['counts'].append(counts)
        df_missing = pd.DataFrame.from_dict(missing)
        self.df = pd.concat([self.df, df_missing])
        self.df = self.reset_sort(df=self.df)
        return

    def reconcile_counts(self: Self, parent: pd.core.frame.DataFrame) -> None:
        """Compare family/genus reports and reconcile read counts."""
        # APPROACH:
        # Kraken2 MPA style files may report read counts that are only
        # at the parent level when compared to the child level. For
        # example, a parent level read count may be larger than the sum
        # of all of the children read counts at the child level; the
        # difference in counts indicates those reads are only defined at
        # the parent level. We may create new child rows for these
        # missing read counts and label them as "undef" at the child
        # level.
        df_parent = parent.df.copy()
        dfg_parent = df_parent.groupby(
            ['domain', 'kingdom', 'phylum', 'class', 'order', 'family']
        )
        parent_keys = set(dfg_parent.groups.keys())

        df_child = self.df.copy()
        dfg_child = df_child.groupby(
            ['domain', 'kingdom', 'phylum', 'class', 'order', 'family']
        )

        missing: dict = {
            'domain': [],
            'kingdom': [],
            'phylum': [],
            'class': [],
            'order': [],
            'family': [],
            'genus': [],
            'counts': []
        }

        for parent_key in parent_keys:
            df_p = dfg_parent.get_group(parent_key)
            parent_counts = df_p.sum()['counts'].item()
            if parent_key in dfg_child.groups.keys():
                child_counts = dfg_child.get_group(
                    parent_key
                ).sum()['counts'].item()
            else:
                child_counts = 0
            diff_counts = int(parent_counts - child_counts)
            if diff_counts > 0:
                domain, kingdom, phylum, class_, order, family = parent_key
                missing['domain'].append(domain)
                missing['kingdom'].append(kingdom)
                missing['phylum'].append(phylum)
                missing['class'].append(class_)
                missing['order'].append(order)
                missing['family'].append(family)
                missing['genus'].append('undef')
                missing['counts'].append(diff_counts)
            elif diff_counts < 0:
                raise ValueError(
                    'Parent and child read count difference is negative.',
                    diff_counts
                )

        df_missing = pd.DataFrame.from_dict(missing)
        self.df = pd.concat([self.df, df_missing])
        self.df = self.reset_sort(df=self.df)

        return

# __END__
