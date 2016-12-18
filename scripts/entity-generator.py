def generateOutputEntity(body, name):
    entityFile = open("../entities/output/"+ name +".java", 'w')
    entityFile.write("package " + package+";\n\n")
    entityFile.write("public class "+ name + " {\n")
    entityFile.write(body)
    entityFile.write("\n}")
    entityFile.close()

name = input("Entre o nome do arquivo : ")
package = input("Entre o nome do pacote: ")
with open("../entities/input/"+name) as file:
    entity = file.readlines()
entity = entity[1::]
body = '\n\t' + '\n\t'.join(["private " + x.split(" ")[0] + " " + x.split(" ")[1][:-1] + ";\n" for x in entity])
body += '\n\t' + '\n\n\t'.join(["public " + x.split(" ")[0]+" get"+x.split(" ")[1][:-1].capitalize() + "() {\n\t\treturn "+x.split(" ")[1][:-1]+";\n\t}\n"
                   "\n\tpublic void set"+x.split(" ")[1][:-1].capitalize() + "("+x.split(" ")[0] + " "+ x.split(" ")[1][:-1] + ") {\n"
                        + "\t\tthis." + x.split(" ")[1][:-1]+" = " + x.split(" ")[1][:-1] + "; \n\t}"
                   for x in entity])
generateOutputEntity(body,name)