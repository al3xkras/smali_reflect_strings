import os
import re

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

ignored_classes = [
    "trace"
]

primitive_types = "ZBSCIJFD"

with open("./reflect.smali", "r") as f:
    reflect_strings = f.read()


def strip_line(i_):
    return lines[i_].strip()


def get_parameters(signature: str):
    signature = signature.split("(")[1].split(")")[0]
    return [x[0] for x in re.finditer(r'(L[^;]+;)|([ZBSCIJFD])', signature)]


def method_predicate(signature):
    is_valid = signature is not None and \
               "abstract" not in signature and \
               "native" not in signature
    if not is_valid:
        return False
    if any(x in signature for x in ignored_methods):
        return False
    return not is_ignored_method(signature)


def is_static_method(signature):
    return "static" in signature


def handle_locals(file_, class_name: str, method_signature: str, current_line: str):
    locals_count = int(current_line.split()[1])
    file_.write("\n    .locals {}\n".format(locals_count))

    p0 = 0 if is_static_method(method_signature) else 1
    params = get_parameters(method_signature)

    # print("METHOD:",method_signature)

    if class_name is not None:
        for j, p in enumerate(params):
            if p in primitive_types:
                continue
            file_.write(
                f"    invoke-static {{p{p0 + j}}}, L{class_name};->reflectStringArguments(Ljava/lang/Object;)V\n")


def handle_method(file_, lines_, line, i, reflection_methods_added):
    method_signature = line

    if not reflection_methods_added and method_predicate(line):
        file_.write("\n" + reflect_strings + "\n")
        reflection_methods_added = True

    file_.write(lines_[i])

    return method_signature, reflection_methods_added


def handle_class(file_, lines_, line, i):
    class_ = line.split()[-1][1:-1]
    pkg = ".".join(class_.split(".")[:-1])

    print("CLASS: ", class_, pkg)

    file_.write(lines_[i])
    return class_, pkg


def patch(file_, lines_: list[str]):
    i = 0

    class_name = None
    method_signature = None
    package_name = None

    reflection_methods_added = False

    while i < len(lines_):

        l_i = strip_line(i)

        if l_i.startswith(".class"):
            class_name, package_name = \
                handle_class(file_, lines_, l_i, i)
            i += 1
            continue

        if l_i.startswith(".method"):
            method_signature, reflection_methods_added = \
                handle_method(file_, lines_, l_i, i, reflection_methods_added)
            i+=1
            continue

        if l_i.startswith(".locals") and method_predicate(method_signature):
            handle_locals(file_, class_name, method_signature, l_i)
            i += 1
            continue

        file_.write(lines_[i])
        i += 1


def is_ignored_package(package):
    out=any(x in package for x in ignored_packages)
    if out:
        print("package ignored:", package)

def is_ignored_method(method):
    out = any(x in method for x in ignored_methods)
    if out:
        print("method ignored:", method)
    return out

def is_ignored_class(class_):
    out=any(x in class_ for x in ignored_classes)
    if out:
        print("class ignored:", class_)
    return out

if __name__ == '__main__':
    for root, dir_, filenames in os.walk(directory):

        if is_ignored_package(root):
            print("package ignored:", root)
            continue

        for filename_ in filenames:
            filename = os.path.join(root, filename_)

            if filename.endswith(".smali"):
                if is_ignored_class(filename):
                    continue

                filepath = os.path.join(directory, filename)

                with open(filepath, "r") as file:
                    lines = file.readlines()

                with open(filepath, "w") as file:
                    patch(file, lines)
