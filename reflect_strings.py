import os
import re

# directory path of the .smali files
directory = "./"

ignored_packages = [
    "google", "android",
    "kotlin", "kotlinx",
    "java", "javax",
]

ignored_methods = [
    "checkForString",
    "reflectStringArguments",
    "reflectStringArgumentsRecursive",
    "MainActivity"
]

primitive_types="ZBSCIJFD"


with open("./reflect.smali", "r") as f:
    reflect_strings = f.read()


def strip_line(i_):
    return lines[i_].strip()


def get_parameters(signature: str):
    signature = signature.split("(")[1].split(")")[0]
    return [x[0] for x in re.finditer(r'(L[^;]+;)|([ZBSCIJFD])', signature)]


def method_predicate(signature):
    is_valid_signature = not "abstract" in signature \
                         and not "native" in signature
    if not is_valid_signature:
        return False
    if any(x in signature for x in ignored_methods):
        return False
    return True


def is_static_method(signature):
    return "static" in signature


if __name__ == '__main__':

    for root, dir_, filenames in os.walk(directory):
        if any(x in root for x in ignored_packages):
            print("package ignored:", root)
            continue
        for filename_ in filenames:
            filename = os.path.join(root, filename_)
            if "trace" in filename:
                continue
            print(filename)
            package_name = ""
            if filename.endswith(".smali"):
                filepath = os.path.join(directory, filename)

                with open(filepath, "r") as file:
                    lines = file.readlines()

                with open(filepath, "w") as file:
                    i = 0

                    class_name = None
                    reflection_methods_added = False
                    method_signature=None
                    while i < len(lines):
                        l_i = strip_line(i)
                        if l_i.startswith(".class"):
                            class_name = l_i.split()[-1][1:-1]
                            package_name = ".".join(class_name.split(".")[:-1])
                            print("CLASS: ", class_name, package_name)

                            file.write(lines[i])
                            i += 1
                            continue

                        if l_i.startswith(".method"):
                            method_signature = l_i

                        if l_i.startswith(".method") and not reflection_methods_added and method_predicate(l_i):
                            if all(x not in l_i for x in ignored_methods):
                                file.write("\n" + reflect_strings + "\n" + lines[i])
                            else:
                                file.write(lines[i])
                            i += 1
                            reflection_methods_added = True
                            continue

                        if l_i.startswith(".locals") and method_signature:
                            locals_count = int(l_i.split()[1])
                            file.write("\n    .locals {}\n".format(locals_count))

                            p0 = 0 if is_static_method(method_signature) else 1
                            params = get_parameters(method_signature)

                            #print("METHOD:",method_signature)

                            if class_name is not None:
                                for j,p in enumerate(params):
                                    if p in primitive_types:
                                        continue
                                    file.write(f"    invoke-static {{p{p0+j}}}, L{class_name};->reflectStringArguments(Ljava/lang/Object;)V\n")

                            i += 1
                            continue

                        file.write(lines[i])
                        i += 1
