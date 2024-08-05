# ComfyUI Nader Tagging
A small set of useful nodes which aid with the tagging process by splitting tags and strings, alternating tags from multiple sources and removing duplicates.

**To install, clone this repo into custom_modules**
cd ComfyUI/custom_nodes
git clone https://github.com/NMWave/ComfyUI-Nader-Tagging

**Tag Alternating Combiner**
Takes input from multiple fields and round robins them according to their ratio.
For instance, if Field 1 has 20 tags, and Field 2 has 5 tags, 4 tags are taken from field 1, then 1 tag taken from field 2, and this is repeated.
<img width="770" alt="image" src="https://github.com/user-attachments/assets/820a056a-1c9b-4fca-9fc3-380063203ce5">


**String Replace**
Simple string replacer, great for replacing individual tag words with an entire sentence.
<img width="1103" alt="image" src="https://github.com/user-attachments/assets/45d9615d-6d96-46a9-9db6-709b85a9e860">


**Tag Duplicates Remover**
Define a delimiter and remove duplicate tags, only the first instance of a tag is kept.
<img width="986" alt="image" src="https://github.com/user-attachments/assets/05d045c4-d87f-4e09-bbf2-9cb4a9c6d8d8">


**Split Tags / Split Sentences**
Split a field of tags into 2 sets, define the max number before splitting.
A version exists for sentence splitting.
<img width="973" alt="image" src="https://github.com/user-attachments/assets/e6eb26cc-3c19-490c-84b2-84aa32356a87">
<img width="774" alt="image" src="https://github.com/user-attachments/assets/1208cfe1-147f-4caa-9369-c3715383fdb4">


**TokenCounter**
Counts the number of tokens (words) in a given field.
<img width="841" alt="image" src="https://github.com/user-attachments/assets/e5d4d175-062d-4ad9-ade2-b465ccb83012">

