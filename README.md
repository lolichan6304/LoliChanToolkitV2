# LoliChanToolkit

## Requirements

The following packages are required for using the above library

You may install using `pip install -r requirements.txt`

```python
numpy
PIL
cv2
requests
lxml
```

## Database Folder Structure

The database is required to be in the below structure

```python
database
    series_title
        chapter_title
            pic_001
            pic_002
        chapter_title
            pic_001
    series_title
        ...
```

As sort is used, it is best to ensure that page numbers are padded with 0, i,e, `01` instead of `1`

## Usage Instructions

For a list of available tools, type `python main.py -h`

Suppose you want to use tool XXX, to get the list of adjustable inputs for XXX, type `python main.py XXX -h`

### Initial Build

An initial build can be done after downloading the directory using `python main.py build`.

### Merge Tool

The default command can be done using `python main.py merge_tool`. This merges list of images from database folder to the local folder such that max height is about 40000 (default)

To start, place the folders you want to merge in the `./database` folder based on the directory listed above. The output will be merged images in the `./local` folder.

For example, given the below input

```python
database
    series_title
        chapter_title
            pic_001
            pic_002
        chapter_title
            pic_001
    series_title
        ...
```

We get output directory in local directory

```python
local
    series_title
        chapter_title
            compic_001
            ...
        chapter_title
            compic_001
    series_title
        ...
```

### Split Tool

The default command can be done using `python main.py split_tool`. This splits list of images from folder to the output folder such that max height is cut at 10000 (default)

To start, place the folders you want to split in the `./split_tool/to_split` folder based on the directory listed above. The output will be split images in the `./split_tool/output` folder.

For example, given the below input

```python
to_split
    series_title
        chapter_title
            pic_001
            pic_002
        chapter_title
            pic_001
    series_title
        ...
```

We get output directory in output directory

```python
output
    series_title
        chapter_title
            compic_001
            ...
        chapter_title
            compic_001
    series_title
        ...
```


## Done by LoliChan6304 :D