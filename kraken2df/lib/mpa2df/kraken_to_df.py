# Project     : kraken2df
# File Name   : kraken_to_df.py
# Description : Converts a Kraken2 report to a dataframe.
# Author      : Todd N. Wylie
# Email       : twylie@wustl.edu
# Created     : Thu May 16 14:37:00 CDT 2024
# Copyright   : Copyright (C) 2024 by T.N. Wylie. All rights reserved.

import pathlib
import pandas as pd  # type: ignore
from typing_extensions import Self

DF_REPORT = 'report_mpa_taxonomy.df.tsv'


class KrakenToDataframe:

    def __init__(self: Self, mpa: pathlib.Path,
                 write_dir_path: pathlib.Path) -> None:
        self.mpa_path = mpa
        self.write_dir_path = write_dir_path
        self.df: pd.core.frame.DataFrame
        self.df_path: pathlib.Path
        return

    def parse_mpa_report(self: Self):

        # We may parse the MPA style report, line-by-line, and expand the
        # pipe-delimited taxonomy lineage across all possible taxon
        # categories.
        #
        # The following categories are expected/supported:
        #
        # (D)omain  : d__
        # (K)ingdom : k__
        # (P)hylum  : p__
        # (C)lass   : c__
        # (O)rder   : o__
        # (F)amily  : f__
        # (G)enus   : g__
        # (S)pecies : s__
        #
        # NOTE: The following categories are not supported in MPA style
        # format:
        #
        # (U)nclassified
        # (R)oot

        with open(self.mpa_path, 'r') as fhi:

            domain_token = 'd__'
            kingdom_token = 'k__'
            phylum_token = 'p__'
            class_token = 'c__'
            order_token = 'o__'
            family_token = 'f__'
            genus_token = 'g__'
            species_token = 's__'

            domain_col = list()
            kingdom_col = list()
            phylum_col = list()
            class_col = list()
            order_col = list()
            family_col = list()
            genus_col = list()
            species_col = list()
            counts_col = list()

            for line in fhi:

                line = line.strip()
                lineage, lineage_count = line.split('\t')
                count = int(lineage_count)
                lineage_f = lineage.split('|')

                domain_tax = None
                kingdom_tax = None
                phylum_tax = None
                class_tax = None
                order_tax = None
                family_tax = None
                genus_tax = None
                species_tax = None

                # Are the all of the taxonomic categories defined? If
                # defined, set the appropriate category value, else it
                # remains None type.

                for taxon in lineage_f:
                    if taxon.startswith(domain_token):
                        domain_tax = taxon
                    elif taxon.startswith(kingdom_token):
                        kingdom_tax = taxon
                    elif taxon.startswith(phylum_token):
                        phylum_tax = taxon
                    elif taxon.startswith(class_token):
                        class_tax = taxon
                    elif taxon.startswith(order_token):
                        order_tax = taxon
                    elif taxon.startswith(family_token):
                        family_tax = taxon
                    elif taxon.startswith(genus_token):
                        genus_tax = taxon
                    elif taxon.startswith(species_token):
                        species_tax = taxon
                    else:
                        raise ValueError(
                            'Taxon has unknown prefix token.',
                            taxon
                        )

                if count is None or type(count) != int:
                    raise TypeError(
                        'Count value is not an integer or is blank.',
                        count
                    )

                domain_col.append(domain_tax)
                kingdom_col.append(kingdom_tax)
                phylum_col.append(phylum_tax)
                class_col.append(class_tax)
                order_col.append(order_tax)
                family_col.append(family_tax)
                genus_col.append(genus_tax)
                species_col.append(species_tax)
                counts_col.append(count)

            # Create a new dataframe to hold the revised information.

            df = pd.DataFrame()
            df['domain'] = domain_col
            df['kingdom'] = kingdom_col
            df['phylum'] = phylum_col
            df['class'] = class_col
            df['order'] = order_col
            df['family'] = family_col
            df['genus'] = genus_col
            df['species'] = species_col
            df['counts'] = counts_col
            self.df = df

            # Write the dataframe to disk for reference.

            self.df_path = self.write_dir_path / DF_REPORT
            self.df.to_csv(self.df_path, sep='\t', index=False)

        return

# __END__
