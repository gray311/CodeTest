def update_record(table, record_id, operation_dict):
    """
    Updates a record in the database by either deleting or inserting characters.

    :param table: Name of the database table.
    :param record_id: ID of the record to update.
    :param operation_dict: Dictionary containing the column updates. 
                           Each key is a column name, and each value is a dictionary 
                           with 'operation' ('insert' or 'delete') and 'position', 'chars' keys.
    """
    sql_queries = []
    
    for column, ops in operation_dict.items():
        operation = ops.get('operation')
        position = ops.get('position')
        chars = ops.get('chars')
        
        if operation == 'insert':
            sql_query = f"UPDATE {table} SET {column} = SUBSTRING({column}, 1, {position}) || '{chars}' || SUBSTRING({column}, {position} + 1) WHERE id = {record_id};"
        elif operation == 'delete':
            sql_query = f"UPDATE {table} SET {column} = SUBSTRING({column}, 1, {position} - 1) || SUBSTRING({column}, {position} + len('{chars}')) WHERE id = {record_id};"
        else:
            continue
        
        sql_queries.append(sql_query)
    
    return sql_queries

# Example usage:
# table = "users"
# record_id = 1
# operation_dict = {
#     "username": {"operation": "insert", "position": 3, "chars": "x"},
#     "bio": {"operation": "delete", "position": 5, "chars": " "}
# }
# queries = update_record(table, record_id, operation_dict)
# for query in queries:
#     print(query)