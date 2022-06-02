import sys
import gzip
import re
import json

# CellLine
# Chemical
# Chromosome
# CopyNumberVariant
# DNAMutation
# Disease
# Gene
# GenomicRegion
# ProteinMutation
# RefSeq
# SNP
# Species

pattern = re.compile(r'^\d+\|')

with gzip.open('../bioconcepts2pubtatorcentral.offset.gz', mode='rt', encoding='utf-8') as f:
  print('[')
  first_line = True
  text = ""
  pmid = ""
  denotation_count = 0
  denotations = []
  attributes  = []
  for line in f:
    l = line.rstrip()
    if len(l) == 0:
#      print(denotations)
#      print(attributes)
      if len(denotations) > 0:
        if first_line:
          first_line = False
        else:
          print(',')
        if len(attributes) > 0:
          print(json.dumps({"sourcedb":"PubMed", "sourceid":pmid, "text" : text, "denotations" : denotations, "attributes" : attributes}))
        else:
          print(json.dumps({"sourcedb":"PubMed", "sourceid":pmid, "text" : text, "denotations" : denotations}))
      text = ""
      denotation_count = 0
      denotations = []
      attributes = []
    else:
      if pattern.match(l):
        vals = l.split('|')
        pmid = vals[0]
        if len(vals[2]) > 0:
          if len(text) > 0:
            text += " "
          text += vals[2]
      else:
        row = l.split('\t')
        pred = row[4].lower()
        id = row[0] + '_' + str(denotation_count)
        attr_id = row[0] + '_' + str(denotation_count) + '_' + row[4]
        denotation = {"id" : id, "span" : {"begin" : int(row[1]), "end" : int(row[2])}, "obj" : row[4]}
#        print(denotation)
        denotations.append(denotation)
        if len(row) == 6 and row[5] != '-':
          attribute  = {"id" : attr_id, "subj" : id, "pred" : pred, "obj" : row[5]}
#          print(attribute)
          attributes.append(attribute)
        denotation_count += 1
  print(']')

f.close()
