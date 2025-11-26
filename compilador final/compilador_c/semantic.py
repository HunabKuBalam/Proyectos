# Lista global de errores semánticos
errors_semanticos = []

def check_declaration(var, symbol_table, lineno):
    """
    Verifica si una variable fue declarada antes de usarse.
    Si no está en la tabla de símbolos, se agrega un error semántico.
    """
    if var not in symbol_table:
        errors_semanticos.append((f"Error semántico: variable '{var}' no declarada", lineno))

def check_assignment(var, value_type, symbol_table, lineno):
    """
    Verifica si el tipo de la variable coincide con el tipo del valor asignado.
    Si hay incompatibilidad, se agrega un error semántico.
    """
    declared_type = symbol_table.get(var)
    if declared_type and (value_type is not None) and declared_type != value_type:
        errors_semanticos.append((f"Error semántico: tipo incompatible en asignación a '{var}'", lineno))
