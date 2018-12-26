# ImmunoProbs Python package uses a simplified manner for calculating the
# generation probability of V(D)J and CDR3 sequences.
# Copyright (C) 2018 Wout van Helvoirt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Contains I/O related functions used in immuno_probs."""


import os

from Bio.SeqIO.FastaIO import SimpleFastaParser
import pandas

from immuno_probs.util.constant import get_separator, get_working_dir
from immuno_probs.util.exception import SeparatorNotValidException


def read_fasta_as_dataframe(infile):
    """Creates a pandas.DataFrame from the FASTA file.

    The dataframe contains header name and sequence columns containing the
    corresponding FASTA data.

    Parameters
    ----------
    infile : string
        Location of the FASTA file to be read in.

    """
    # Create a dataframe and read in the fasta file.
    fasta_df = pandas.DataFrame(columns=['header', 'sequence'])
    with open(infile, 'r') as fasta_file:
        for title, sequence in SimpleFastaParser(fasta_file):
            fasta_df = fasta_df.append({
                'header': title,
                'sequence': sequence.upper(),
            }, ignore_index=True)
    return fasta_df


def read_csv_to_dataframe(filename):
    """Read in a CSV file as pandas.DataFrame.

    Parameters
    ----------
    filename : string
        Filename to be read in as dtaframe.

    Notes
    -----
        This function uses the global SEPARATOR variable to set the separator
        string for the input CSV file. Comments ('#') in the file are skipped.

    """
    dataframe = pandas.read_csv(filename, sep=get_separator(), comment='#',
                                header=0)
    return dataframe


def write_dataframe_to_csv(dataframe, filename):
    """Writes a pandas.DataFrame to a CSV formatted file.

    The output CSV file is comma separated (default) and if the file already
    exists, a number will be appended to the filename. The given output directory
    is created recursively if it does not exist. The column names in the dataframe
    is used as first line in the csv file.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The dataframe to be written to the CSV file.
    filename : string
        Base filename for writting the file, excluding the '.csv' extension.

    Returns
    -------
    tuple
        Containing the output directory and the name of the file that has been
        written to disk.

    Raises
    ------
    SeparatorNotValidException
        When the SEPARATOR global variable is not of type string.

    Notes
    -----
        This function uses the global SEPARATOR variable to set the separator
        string for the output CSV file.

    """
    # Check out available worker count and adjust accordingly.
    separator = get_separator()
    if not isinstance(separator, str):
        raise SeparatorNotValidException("The SEPARATOR variable needs to be " \
                                         "of type string", separator)

    # Create directory's recursively if not exists.
    directory = get_working_dir()
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    # Check if the filename is unique, modify name if necessary.
    file_count = 1
    updated_filename = filename

    # Keep modifying the filename until it doesn't exist.
    while os.path.isfile(os.path.join(directory, updated_filename + '.csv')):
        updated_filename = str(filename) + '_' + str(file_count)
        file_count += 1

    # Write dataframe contents to csv file and return info.
    pandas.DataFrame.to_csv(dataframe, path_or_buf=os.path.join(
        directory, updated_filename + '.csv'), sep=separator, index=False)
    return (directory, updated_filename + '.csv')
