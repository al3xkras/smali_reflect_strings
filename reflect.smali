
.method public static checkForString(Ljava/lang/Object;I)Z
    .locals 3
    .param p0, "o"    # Ljava/lang/Object;
    .param p1, "depth"    # I

    .line 29
    const/4 v0, 0x0

    if-nez p0, :cond_0

    .line 30
    return v0

    .line 31
    :cond_0
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    const-class v2, Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_1

    .line 32
    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "[depth="

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "], next arg: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 33
    const/4 v0, 0x1

    return v0

    .line 35
    :cond_1
    return v0
.end method

.method public static reflectStringArguments(Ljava/lang/Object;)V
    .locals 7
    .param p0, "obj"    # Ljava/lang/Object;

    .line 57
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Thread;->getStackTrace()[Ljava/lang/StackTraceElement;

    move-result-object v0

    .line 58
    .local v0, "trace":[Ljava/lang/StackTraceElement;
    const/4 v1, 0x3

    .line 59
    .local v1, "i":I
    array-length v2, v0

    add-int/lit8 v3, v1, 0x1

    if-ge v2, v3, :cond_0

    .line 60
    return-void

    .line 61
    :cond_0
    aget-object v2, v0, v1

    .line 62
    .local v2, "s":Ljava/lang/StackTraceElement;
    const-string v3, " "

    .line 63
    .local v3, "space":Ljava/lang/String;
    sget-object v4, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "METHOD: "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v2}, Ljava/lang/StackTraceElement;->getClassName()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v2}, Ljava/lang/StackTraceElement;->getMethodName()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 64
    const/4 v4, 0x0

    invoke-static {p0, v4}, L{class_name};->checkForString(Ljava/lang/Object;I)Z

    move-result v5

    if-nez v5, :cond_1

    .line 65
    invoke-static {p0, v4}, L{class_name};->reflectStringArgumentsRecursive(Ljava/lang/Object;I)V

    .line 66
    :cond_1
    return-void
.end method

.method public static reflectStringArgumentsRecursive(Ljava/lang/Object;I)V
    .locals 7
    .param p0, "obj"    # Ljava/lang/Object;
    .param p1, "depth"    # I

    .line 39
    const/4 v0, 0x1

    .line 40
    .local v0, "MAX_DEPTH":I
    if-le p1, v0, :cond_0

    .line 41
    return-void

    .line 42
    :cond_0
    if-nez p0, :cond_1

    .line 43
    return-void

    .line 44
    :cond_1
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/Class;->getDeclaredFields()[Ljava/lang/reflect/Field;

    move-result-object v1

    array-length v2, v1

    const/4 v3, 0x0

    :goto_0
    if-ge v3, v2, :cond_3

    aget-object v4, v1, v3

    .line 45
    .local v4, "field":Ljava/lang/reflect/Field;
    const/4 v5, 0x1

    invoke-virtual {v4, v5}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 47
    :try_start_0
    invoke-virtual {v4, p0}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v5

    .line 48
    .local v5, "value":Ljava/lang/Object;
    invoke-static {v5, p1}, L{class_name};->checkForString(Ljava/lang/Object;I)Z

    move-result v6

    if-nez v6, :cond_2

    .line 49
    add-int/lit8 v6, p1, 0x1

    invoke-static {v5, v6}, L{class_name};->reflectStringArgumentsRecursive(Ljava/lang/Object;I)V
    :try_end_0
    .catch Ljava/lang/IllegalAccessException; {:try_start_0 .. :try_end_0} :catch_0

    .line 52
    .end local v5    # "value":Ljava/lang/Object;
    :cond_2
    goto :goto_1

    .line 50
    :catch_0
    move-exception v5

    .line 51
    .local v5, "e":Ljava/lang/IllegalAccessException;
    invoke-virtual {v5}, Ljava/lang/IllegalAccessException;->printStackTrace()V

    .line 44
    .end local v4    # "field":Ljava/lang/reflect/Field;
    .end local v5    # "e":Ljava/lang/IllegalAccessException;
    :goto_1
    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    .line 54
    :cond_3
    return-void
.end method
