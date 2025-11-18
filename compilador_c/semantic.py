def check_declaration(var, symbol_table, lineno):
    if var not in symbol_table:
        from gui import log_error
        log_error(f"Error semántico: variable '{var}' no declarada", lineno)

def check_assignment(var, value_type, symbol_table, lineno):
    declared_type = symbol_table.get(var)
    if declared_type and declared_type != value_type:
        from gui import log_error
        log_error(f"Error semántico: tipo incompatible en asignación a '{var}'", lineno)
