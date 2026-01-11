from markdown import markdown

output = markdown('''
# Step 1
## Step 2
* item 1
* item 2
Visitez [IUT de Roanne](https://iut-roanne.univ-st-etienne.fr/fr/index.html)
''')

print(output)
