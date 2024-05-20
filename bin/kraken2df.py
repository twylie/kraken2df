#!/usr/bin/python3

# Project     : kraken2df
# File Name   : kraken2df.py
# Description : Parsing and reporting of Kraken2 MPA format files.
# Author      : Todd N. Wylie
# Email       : twylie@wustl.edu
# Created     : Mon May 13 09:47:51 CDT 2024
# Copyright   : Copyright (C) 2024 by T.N. Wylie. All rights reserved.

"""
Parse the Kraken2 report and split into separate taxonomy reports.

The following individual reports will be generated and collected into a
TaxonomyReports object, which will be returned from this function.

1. Domain
2. Kingdom
3. Phylum
4. Class
5. Order
6. Family
7. Genus
8. Species

The full versions of the reports will be stored, which include undefined
taxa and zero-count entries. Methods will be prtovided to handle any
manipulation of the reports such as removing zero-count entries or
sort-order specifics.
"""

import kraken2df
from pathlib import Path
import shutil

# PARSE KRAKEN2 REPORT FILE ###################################################

# Load and evaluate the command line arguments. Create a directory for
# writing all of the downstream report files. Parse the Kraken2
# MPA-style report file and create an associated dataframe
# representation of the information.

args = kraken2df.CommandLineArguments()
args.write_dir_path.mkdir()


kdf = kraken2df.KrakenToDataframeMPA(
    report=args.report_path,
    write_dir_path=args.write_dir_path
)
kdf.parse_mpa_report()

# COLLECT READ COUNTS #########################################################

# Collect category-level read counts and populate corresponding report
# dataframes. We remove rows from the original input dataframe as we
# iterate through count collection.

reports = kraken2df.TaxonomyReports(sample_id=args.sample_id, df=kdf.df.copy())
reports.df = reports.domain.collect_counts(df=reports.df)
reports.df = reports.kingdom.collect_counts(df=reports.df)
reports.df = reports.phylum.collect_counts(df=reports.df)
reports.df = reports.class_.collect_counts(df=reports.df)
reports.df = reports.order.collect_counts(df=reports.df)
reports.df = reports.family.collect_counts(df=reports.df)
reports.df = reports.genus.collect_counts(df=reports.df)
reports.df = reports.species.collect_counts(df=reports.df)

# APPEND UNDEFINED READ COUNTS ################################################

# Evaluate each category-level and carry-forward any missing entries
# from the preceding reports. This should help to ensure that the total
# number of reads are accounted for across the reports.

reports.kingdom.append_to_counts(domain=reports.domain.df)
reports.phylum.append_to_counts(kingdom=reports.kingdom.df)
reports.class_.append_to_counts(phylum=reports.phylum.df)
reports.order.append_to_counts(class_=reports.class_.df)
reports.family.append_to_counts(order=reports.order.df)
reports.genus.append_to_counts(family=reports.family.df)
reports.species.append_to_counts(genus=reports.genus.df)

# RECONCILE READ COUNTS #######################################################

# Reconcile the read counts in terms of "unclassified" reads at the
# report level---i.e., if the read counts are higher for the parent
# level, add the difference to the current category level as undef. All
# of the reports should have the same number of total reads when this
# process is completed.

reports.kingdom.reconcile_counts(parent=reports.domain)
reports.phylum.reconcile_counts(parent=reports.kingdom)
reports.class_.reconcile_counts(parent=reports.phylum)
reports.order.reconcile_counts(parent=reports.class_)
reports.family.reconcile_counts(parent=reports.order)
reports.genus.reconcile_counts(parent=reports.family)
reports.species.reconcile_counts(parent=reports.genus)
reports.compare_report_read_totals()

# WRITE REPORT FILES ##########################################################

# We will be writing report versions for (1) terse, non-zero read counts
# and (2) the full version of the report which includes zero read
# counts.

reports.write_all_terse_reports(outdir=args.write_dir_path)
reports.write_all_verbose_reports(outdir=args.write_dir_path)

# Copy the original Kraken2 report file to the report directory for
# reference.

mpa_input_path = Path(args.report_path)
shutil.copy(
    mpa_input_path,
    args.write_dir_path / mpa_input_path.name
)

# __END__
