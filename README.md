# bloxberg_verify
A Python script which verifies a Bloxberg blockchain timestamp generated with https://certify.bloxberg.org/ or using their [API](https://app.swaggerhub.com/apis/bloxberg/fast-api/0.4.0). This can be used for example to verify Bloxberg blockchain timestamps generated in [ElabFTW](https://github.com/elabftw/elabftw).

## Usage
Just clone this repo, create a virtualenv which fulfils the requirements from requirements.txt and run
~~~bash
python bloxberg_verify <json-filename>
~~~
where json-filename points to the Bloxberg proof json which is attached to their pdf certificates. The json proof can be extracted from the pdf using Adobe Reader or using [poppler's](https://github.com/cbrunet/python-poppler) pdfdetach
~~~bash
pdfdetach -saveall <pdf-filename>
~~~

Example output
~~~
Check that document hash is contained in normalised proof
 success ✓
Check file integrity, i.e. if the merkle root hash encoded in this file is identical to the calculated hash of this file.
 success ✓

Original file hash:  dskalfnkasjhfkjsanbfjlksadf
Merkle root:  98a2ba3cdc314cb5ef0b566daff91e561f4b7bcb55923ae0be771fece3774ac9
Transaction id:  0x21c6fbb2653bcb48f8e21bf2beee7c641f30d53f637e2bf7cef8810c7a3c39d3

Check if transaction exists in the blockchain and if it contains the merkle root
 success ✓
Hashes match. The file is properly timestamped on the bloxberg blockchain. The block timestamp is 2024-02-28 12:29:00 and the number of block confirmations is 330.
~~~


## License
Copyright (c) 2024 Tobias E. Naegele

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
