# DocumentSummarizer
Simple document summarization tool that summarizes documents using LDA

This tool serves as a simple demo showcasing how topic modelling can be used to summarize documents. This tool uses LDA to discover topics and then summarizes the document by selecing sentences from each topic.

## Setup:
First, clone this repo and cd into the cloned directory. Then, inside the directory, run:
```
pip install .
```
to install the required dependencies.
  

## Usage:
### When running from the command line:
The general format for the command is:
```
./summarize.py [options]
```
#### Supported flags and options:
| Flag/Option | Description |
| --- | --- |
| --src= | By default, the script takes input from stdin. Alternatively the path to a file can be supplied here. |
| --from_url | This flag indicates that the string passed using the `--src` option is a web URL. The script will scrape content from the webpage and try summarizing that. |
| --tokenize_sentences | By default, the script splits the document into multiple paragraph to apply LDA. Specifying this flag will split the document into sentences instead |
| --num_topics= | The number of topics we should try to discover in the document. This will also be the maximum number paragraphs or sentences we will have in the summary |
| --print_topics | Print the discovered topics instead of the summary |

#### Examples:

```
./summarize.py --from_url --src=https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation
```
This will make DocumentSummarizer download the webpage from the given url, scrape the text from the webpage and pick the most important paragraphs to summarize the document.

For even shorter summaries, it is recommended to use the `--tokenize_sentences` option to process the document sentence-wise and pick the most important sentences instead, as shown below:
```
./summarize.py --from_url --tokenize_sentences --src=https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation
```
This requires the nltk PunktWordTokenizer tokenizer to be installed. The tool will automatically download the tokenizer data if it's not already available.
Text data can also be piped into the script like so:
```
cat file.txt | ./summarize.py
```
This allows us to do things like trying to summarize log files. For example, we can try analyzing kernel logs for the current boot to figure out what the most typical messages look like by running:
```
journalctl -xek | ./summarize.py 
```

### Importing DocumentSummarizer as a library:
```
>>> import LDASummarizer
>>> corpus = [
... "In natural language processing, the latent Dirichlet allocation (LDA) is a generative statistical model that allows sets of observations to be explained by unobserved groups that explain why some parts of the data are similar. For example, if observations are words collected into documents, it posits that each document is a mixture of a small number of topics and that each word's presence is attributable to one of the document's topics. LDA is an example of a topic model and belongs to the machine learning toolbox and in wider sense to the artificial intelligence toolbox.",
... "In the context of population genetics, LDA was proposed by J. K. Pritchard, M. Stephens and P. Donnelly in 2000.",... "LDA was applied in machine learning by David Blei, Andrew Ng and Michael I. Jordan in 2003.",
... "In evolutionary biology and bio-medicine, the model is used to detect the presence of structured genetic variation in a group of individuals. The model assumes that alleles carried by individuals under study have origin in various extant or past populations. The model and various inference algorithms allow scientists to estimate the allele frequencies in those source populations and the origin of alleles carried by individuals under study. The source populations can be interpreted ex-post in terms of various evolutionary scenarios. In association studies, detecting the presence of genetic structure is considered a necessary preliminary step to avoid confounding."
... ]
>>> summarizer = LDASummarizer.LDASummarizer(corpus)
>>> summarizer.get_summary()
"In natural language processing, the latent Dirichlet allocation (LDA) is a generative statistical model that allows sets of observations to be explained by unobserved groups that explain why some parts of the data are similar. For example, if observations are words collected into documents, it posits that each document is a mixture of a small number of topics and that each word's presence is attributable to one of the document's topics. LDA is an example of a topic model and belongs to the machine learning toolbox and in wider sense to the artificial intelligence toolbox.\n\nIn the context of population genetics, LDA was proposed by J. K. Pritchard, M. Stephens and P. Donnelly in 2000.\n\nLDA was applied in machine learning by David Blei, Andrew Ng and Michael I. Jordan in 2003.\n\nIn evolutionary biology and bio-medicine, the model is used to detect the presence of structured genetic variation in a group of individuals. The model assumes that alleles carried by individuals under study have origin in various extant or past populations. The model and various inference algorithms allow scientists to estimate the allele frequencies in those source populations and the origin of alleles carried by individuals under study. The source populations can be interpreted ex-post in terms of various evolutionary scenarios. In association studies, detecting the presence of genetic structure is considered a necessary preliminary step to avoid confounding."
```
