# Project     : kraken2df
# File Name   : taxonomy_reports.py
# Description : A collection of Kraken2 MPA taxonomy reports and methods.
# Author      : Todd N. Wylie
# Email       : twylie@wustl.edu
# Created     : Mon May 13 10:24:47 CDT 2024
# Copyright   : Copyright (C) 2024 by T.N. Wylie. All rights reserved.

import pandas as pd  # type: ignore
from typing_extensions import Self
from pathlib import Path
from . domain_report import DomainReport  # type: ignore
from . kingdom_report import KingdomReport  # type: ignore
from . phylum_report import PhylumReport  # type: ignore
from . class_report import ClassReport  # type: ignore
from . order_report import OrderReport  # type: ignore
from . family_report import FamilyReport  # type: ignore
from . genus_report import GenusReport  # type: ignore
from . species_report import SpeciesReport  # type: ignore


class TaxonomyReports():
    """A collection of parsed Kraken2 taxonomy reports.

    This class is a container for a collection of individual Kraken2
    taxonomy reports based on a single input Kraken2 MPA-style report.
    Methods are provided for handling, printing, and saving the reports.
    The following reports are available through the class methods:
    domain, kingdom, phylum, class, order, family, genus, ans species.
    """

    def __init__(
            self: Self,
            sample_id: str,
            df: pd.core.frame.DataFrame
            ) -> None:
        """Construct the class."""
        df.fillna('undef', inplace=True)
        df['domain'].replace('undef', 'd__Undefined', inplace=True)
        self.df = df
        self.df_original = self.df.copy()
        self.sample_id = sample_id
        self.domain = DomainReport()
        self.kingdom = KingdomReport()
        self.phylum = PhylumReport()
        self.class_ = ClassReport()
        self.order = OrderReport()
        self.family = FamilyReport()
        self.genus = GenusReport()
        self.species = SpeciesReport()
        return

    def compare_report_read_totals(self: Self) -> None:
        """Compare read totals across all report levels."""
        read_counts: set = set()
        read_counts.add(self.domain.calc_total_reads())
        read_counts.add(self.kingdom.calc_total_reads())
        read_counts.add(self.phylum.calc_total_reads())
        read_counts.add(self.class_.calc_total_reads())
        read_counts.add(self.order.calc_total_reads())
        read_counts.add(self.family.calc_total_reads())
        read_counts.add(self.genus.calc_total_reads())
        read_counts.add(self.species.calc_total_reads())
        if len(read_counts) != 1:
            raise ValueError(
                'Total read counts differ among reports.',
                read_counts
            )
        return

    def write_all_terse_reports(self: Self, outdir: Path) -> None:
        """Write all taxonomy levels to a terse, non-zero count report file."""
        outdir_terse = outdir / 'non_zero_reports'
        outdir_terse.mkdir()
        self.domain.format_report(zeros=False)
        self.domain.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.kingdom.format_report(zeros=False)
        self.kingdom.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.phylum.format_report(zeros=False)
        self.phylum.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.class_.format_report(zeros=False)
        self.class_.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.order.format_report(zeros=False)
        self.order.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.family.format_report(zeros=False)
        self.family.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.genus.format_report(zeros=False)
        self.genus.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.species.format_report(zeros=False)
        self.species.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        return

    def write_all_verbose_reports(self: Self, outdir: Path) -> None:
        """Write all taxonomy levels to a verbose (with zeros) report file."""
        outdir_terse = outdir / 'zero_reports'
        outdir_terse.mkdir()
        self.domain.format_report(zeros=True)
        self.domain.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.kingdom.format_report(zeros=True)
        self.kingdom.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.phylum.format_report(zeros=True)
        self.phylum.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.class_.format_report(zeros=True)
        self.class_.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.order.format_report(zeros=True)
        self.order.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.family.format_report(zeros=True)
        self.family.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.genus.format_report(zeros=True)
        self.genus.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        self.species.format_report(zeros=True)
        self.species.save_report(
            sample_id=self.sample_id,
            outdir=outdir_terse.as_posix(),
            index=True
        )
        return

# __END__
