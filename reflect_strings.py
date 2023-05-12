import os

# directory path of the .smali files
directory = "./"

ignored_packages = [
    "google", "android",
    "kotlin", "kotlinx",
    "java", "javax",
]

with open("./reflect.smali", "r") as f:
    reflect_strings = f.read()

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

                def strip_line(i_):
                    return lines[i_].strip()

                def get_parameters_count(signature):
                    try:
                        parameters = signature.split("(")[1].split(")")[0].split(";")[:-1]
                    except IndexError as e:
                        print(e)
                        return 0
                    return len(parameters)

                def method_predicate(signature):
                    is_valid_signature = not "abstract" in signature \
                        and not "native" in signature
                    if not is_valid_signature:
                        return False
                    return get_parameters_count(signature)>0

                class_name = None
                reflection_methods_added = False
                while i < len(lines):
                    l_i = strip_line(i)
                    if l_i.startswith(".class"):
                        class_name = l_i.split()[-1][1:-1]
                        package_name = ".".join(class_name.split(".")[:-1])
                        print("CLASS: ", class_name, package_name)

                        file.write(lines[i])
                        i += 1
                        continue

                    if l_i.startswith(".method") and not reflection_methods_added:
                        if "checkForString" not in l_i:
                            file.write("\n" + reflect_strings + "\n" + lines[i])
                        else:
                            file.write(lines[i])
                        i += 1
                        reflection_methods_added = True
                        continue

                    if l_i.startswith(".locals") and method_predicate(strip_line(i - 1)):
                        locals_count = int(l_i.split()[1])
                        file.write("\n    .locals {}\n".format(locals_count))

                        params = get_parameters_count(strip_line(i - 1))

                        if class_name is not None:
                            for i in range(params):
                                file.write(f"    invoke-static {{p{i}}}, L{class_name};->reflectStringArguments(Ljava/lang/Object;)V\n")

                        i += 1
                        continue

                    file.write(lines[i])
                    i += 1
