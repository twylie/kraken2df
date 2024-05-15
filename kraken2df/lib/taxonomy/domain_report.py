# Project     : kraken2df
# File Name   : domain_report.py
# Description : Domain level report object and methods.
# Author      : Todd N. Wylie
# Email       : twylie@wustl.edu
# Created     : Mon May 13 10:34:21 CDT 2024
# Copyright   : Copyright (C) 2024 by T.N. Wylie. All rights reserved.

import pandas as pd  # type: ignore
from pathlib import Path
from typing_extensions import Self


class DomainReport():
    """Domain level report object and methods."""

    def __init__(self: Self) -> None:
        """Construct the class."""
        self.df: pd.core.frame.DataFrame
        self.df_f: pd.core.frame.DataFrame
        return

    def collect_counts(
            self: Self,
            df: pd.core.frame.DataFrame
            ) -> pd.core.frame.DataFrame:
        """Collect and separate the domain read counts."""
        # APPROACH:
        # 1. Group by domain.
        # 2. Get the first row of the group; this is the count for the
        # group.
        # 3. From the original, full dataframe, remove the rows used for
        # counts based on index ids. As we move to the next level, the
        # count-rows used here are no longer needed.
        drop_cols = [
            'kingdom',
            'phylum',
            'class',
            'order',
            'family',
            'genus',
            'species'
        ]
        dfg = df.groupby('domain')
        df_i = dfg.head(1)
        remove_ids = df_i.index
        df_i = df_i.copy()
        df_i = self.reset_sort(df=df_i)
        df_i.drop(drop_cols, axis=1, inplace=True)
        self.df = df_i.copy()
        df_revised = df.copy()
        df_revised.drop(index=remove_ids, inplace=True)
        return df_revised

    def reset_sort(
            self: Self,
            df: pd.core.frame.DataFrame
            ) -> pd.core.frame.DataFrame:
        """Return a re-indexed and sorted domain report."""
        df = df.copy()
        df['counts'] = df['counts'].astype(int)
        df.sort_values('counts', ascending=False, inplace=True)
        df.reset_index(inplace=True, drop=True)
        return df

    def format_report(
            self: Self,
            undef: bool = True,
            zeros: bool = True
            ) -> None:
        """Populates a formatted dataframe for a report."""
        df = self.df.copy()
        if undef is False:
            df = df.loc[df['domain'] != 'undef']
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
            sample_id: str,
            index: bool = True
            ) -> None:
        """Save a formatted report to a tab-delimited file."""
        counts = self.calc_total_reads_formatted()
        out_dir = Path(outdir)
        out_file = f'01.domain.{counts}.tsv'
        fho = out_dir / out_file
        df = self.df_f.copy()
        df.insert(0, 'sample_id', sample_id)
        df['counts_pct'] = round(
            (df['counts'].apply(lambda x: x / counts)) * 100,
            2
        )
        df.to_csv(fho, sep='\t', index=index)
        return

# __END__
