<!-- Begin document text. -->
<!-- T.N. Wylie -->
<!-- twylie@wustl.edu -->
<!-- version 1.0.0  -->
<!-- Mon Oct  5 09:28:22 CDT 2026  -->

# kraken2df

This code parses Kraken2 reports and splits them into separate, consolidated taxonomy reports. The output from Kraken2 will be parsed and formatted to display consolidated, full lineages of identities, read counts, and percentages by cumulative taxonomic groupings. The full versions of the reports will be stored, which include undefined taxa and zero-count entries. Methods will be provided to handle any manipulation of the reports such as removing zero-count entries or sort-order specifics.

The following individual reports will be generated and collected into a TaxonomyReports object:

1. Domain
2. Kingdom
3. Phylum
4. Class
5. Order
6. Family
7. Genus
8. Species

# Docker

## Docker Image

A corresponding Docker image for `kraken2df` is available at the link provided below.

https://hub.docker.com/r/twylie/kraken2df

## Docker Pull Command

```zsh
docker pull twylie/kraken2df
```

# Running kraken2df

```zsh
kraken2df --help
```

```text
usage: kraken2df.py [-h] [--version] --report FILE --outdir DIR --id STR

Description here.

optional arguments:
  -h, --help     Display the extended usage statement.
  --version      Display the software version number.

required:
  --report FILE  File path to the source Kraken2 report.
  --outdir DIR   Existing directory path to write report files.
  --id STR       Sample id used for labeling reports.
```

# Contact

**Todd N. Wylie, Associate Professor** \
Department of Pediatrics \
Division of Gastroenterology, Hepatology, & Nutrition \
Washington University School of Medicine \
660 S. Euclid Avenue, MSC 8208-0043-10 \
St. Louis, MO 63110 \
email — twylie@wustl.edu

# License

*Begin license text.*

**MIT License**
https://opensource.org/license/mit

Copyright 2024-2026 T.N. Wylie. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*End license text.*

<!-- End document text. -->
