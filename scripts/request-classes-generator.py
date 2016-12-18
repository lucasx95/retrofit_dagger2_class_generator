METHOD = "method"
PATH = "path"
TYPE = "type"
NAME = "name"
FIELDS = "fields"
LOCATION = "location"

METHOD_KEY = [METHOD, PATH, TYPE, NAME, FIELDS]
PARAMETER_KEY = [LOCATION, TYPE, NAME]


# Métodos auxiliares
def getParameters(params):
    return [{PARAMETER_KEY[i]: parameter.split(" ")[i].rstrip('\n') if i > 0 else "Body" if parameter[
                                                                                                0] == "b" else "Path(\"" +
                                                                                                               parameter.split(
                                                                                                                   " ")[
                                                                                                                   2] + "\")"
             for i in range(3)}
            for parameter in params]


def getPathParams(params):
    pathParams = list(filter(lambda p: "Path" in p[LOCATION], params))
    return '/' + '/'.join(["{" + path[NAME] + "}" for path in pathParams]) + '/' if len(pathParams) > 0 else ""


def getParamsString(params):
    return "(" + ', '.join(["@" + param[LOCATION] + " " + param[TYPE] + " " + param[NAME] for param in params]) + ")"


def getMethodString(method):
    return "\t@" + method[METHOD] + "(\"" + method[PATH] + getPathParams(method[FIELDS]) + "\")\n" \
           + "\tCall<" + method[TYPE] + "> " + method[NAME] + getParamsString(method[FIELDS]) + ";\n"


def getMethodSignature(method):
    return method[TYPE] + " " + method[NAME] + "(" + ', '.join(
        ["final " + param[TYPE] + " " + param[NAME] for param in method[FIELDS]]) + ")"


def getDaoInjections(name):
    injectionFieldString = "\tprivate final " + name + "Service " + name.lower() + "Service;\n"
    contructor = "\t@Inject\n\tpublic App" + name + "Dao(@NonNull final " + name + "Service " + name.lower() + "Service) {\n" \
                 + "\t\tthis." + name.lower() + "Service = " + name.lower() + "Service;\n\t}\n"
    return injectionFieldString + '\n' + contructor


def getDaoMethodBody(method, name):
    return "\t\ttry {\n\t\t\tResponse<" + method[
        TYPE] + "> response = " + name.lower() + "Service\n\t\t\t\t." \
           + method[NAME] + "(" + ', '.join([param[NAME] for param in method[FIELDS]]) + ").execute();\n\t\t\t" \
           + "if (response.code() != ResponseConstants.OK) throw new GeneralDaoErrorException(GeneralErrorCode.GENERIC);\n\t\t\t" \
           + "return response.body();\n\t\t" + "} catch (Exception exception) {\n\t\t\t" \
           + "throw new GeneralDaoErrorException(exception.getMessage());\n\t\t}\n"


def getUseCasesInjections(name):
    return '\tpublic ' + name + "Dao " + name[0].lower() + name[
                                                           1::] + "Dao;\n\n\t@Inject\n\tpublic App" + name + "UseCases(@NonNull final " + \
           name + "Dao " + name[0].lower() + name[1::] + "Dao ) {\n\t\tthis." + name[0].lower() + name[1::] + "Dao = " \
           + name[0].lower() + name[1::] + "Dao;\n\t}\n"


def getUseCaseMethodBody(method, name):
    return "\t\ttry {\n\t\t\treturn " + name[0].lower() + name[1::] + "Dao." + method[NAME] + "(" \
           + ', '.join(
        [param[NAME] for param in method[FIELDS]]) + ");\n\t\t" + "} catch (Exception exception) {\n\t\t\t" \
           + "throw new GeneralBusinessErrorException(exception.getMessage());\n\t\t}\n"


# Métodos de impressão
def generateOutputService(methods, name):
    serviceFile = open("../request-classes/output/" + name + "Service.java", 'w')
    serviceFile.write("package " + dataPackage + ";\n\n")
    serviceFile.write("public interface " + name + "Service {\n\n")
    serviceFile.write('\n'.join([getMethodString(m) for m in methods]))
    serviceFile.write("\n}")
    serviceFile.close()


def generateOutputDao(methods, name):
    daoInterface = open("../request-classes/output/" + name + "Dao.java", 'w')
    daoInterface.write("package " + dataPackage + ";\n\n")
    daoInterface.write("public interface " + name + "Dao {\n\n")
    daoInterface.write(
        '\n'.join(['\t' + getMethodSignature(m) + " throws GeneralDaoErrorException;\n" for m in methods]))
    daoInterface.write("\n}")
    daoInterface.close()


def generateOutputDaoImpl(methods, name):
    daoImpl = open("../request-classes/output/App" + name + "Dao.java", 'w')
    daoImpl.write("package " + dataPackage + ";\n\n")
    daoImpl.write("public class App" + name + "Dao implements " + name + "Dao {\n\n")
    daoImpl.write(getDaoInjections(name))
    daoImpl.write('\n' + '\n'.join(['\t@Override\n\tpublic ' + getMethodSignature(
        m) + " throws GeneralDaoErrorException {\n" + getDaoMethodBody(m, name) + "\t}\n"
                                    for m in methods]))
    daoImpl.write("\n}")
    daoImpl.close()


def generateOutputUseCases(methods, name):
    daoInterface = open("../request-classes/output/" + name + "UseCases.java", 'w')
    daoInterface.write("package " + bussinessPackage + ";\n\n")
    daoInterface.write("public interface " + name + "UseCases {\n\n")
    daoInterface.write(
        '\n'.join(['\t' + getMethodSignature(m) + " throws GeneralBusinessErrorException;\n" for m in methods]))
    daoInterface.write("\n}")
    daoInterface.close()


def generateOutputUseCaseImpl(methods, name):
    daoImpl = open("../request-classes/output/App" + name + "UseCases.java", 'w')
    daoImpl.write("package " + bussinessPackage + ";\n\n")
    daoImpl.write("public class App" + name + "UseCases implements " + name + "UseCases {\n\n")
    daoImpl.write(getUseCasesInjections(name))
    daoImpl.write('\n' + '\n'.join(['\t@Override\n\tpublic ' + getMethodSignature(
        m) + " throws GeneralBusinessErrorException {\n" + getUseCaseMethodBody(m, name) + "\t}\n"
                                    for m in methods]))
    daoImpl.write("\n}")
    daoImpl.close()


# Lê entreada e abre o arquivo
name = input("Entre o nome do arquivo : ")
package = input("Entre o nome do pacote: ")
dataPackage = package + ".data"
bussinessPackage = package + ".bussiness"
with open("../request-classes/input/" + name) as file:
    requestClass = file.readlines()
# converte arquivo para lista de dicionario e de injections
methodList = [{METHOD_KEY[i]: m.split(" - ")[i] if i < 4 else getParameters(m.split(" - ")[4::]) for i in range(5)}
              for m in requestClass]
# Gera os arquivos
generateOutputService(methodList, name)
generateOutputDao(methodList, name)
generateOutputDaoImpl(methodList, name)
generateOutputUseCases(methodList, name)
generateOutputUseCaseImpl(methodList, name)
