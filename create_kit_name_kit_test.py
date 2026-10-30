import data
import sender_stand_request

# Función auxiliar para obtener el token de autenticación de un nuevo usuario
def get_new_user_token():
    response = sender_stand_request.post_new_user(data.user_body)
    return response.json()["authToken"]

# Función auxiliar para cambiar el cuerpo del kit con un nombre específico
def get_kit_body(name):
    current_body = data.kit_body.copy()
    current_body["name"] = name
    return current_body

# Prueba 1: El número permitido de caracteres (1)
def test_create_kit_1_letter_in_name_get_success_response():
    kit_body = get_kit_body("a")
    positive_assert(kit_body)

# Prueba 2: El número permitido de caracteres (511)
def test_create_kit_511_letters_in_name_get_success_response():
    long_name = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC"
    kit_body = get_kit_body(long_name)
    positive_assert(kit_body)

# Prueba 3: El número de caracteres es menor que la cantidad permitida (0)
def test_create_kit_0_letters_in_name_get_error_response():
    kit_body = get_kit_body("")
    negative_assert_code_400(kit_body)

# Prueba 4: El número de caracteres es mayor que la cantidad permitida (512)
def test_create_kit_512_letters_in_name_get_error_response():
    too_long_name = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD"
    kit_body = get_kit_body(too_long_name)
    negative_assert_code_400(kit_body)

# Prueba 5: Se permiten caracteres especiales
def test_create_kit_has_special_symbols_in_name_get_success_response():
    kit_body = get_kit_body("№%@\",")
    positive_assert(kit_body)

# Prueba 6: Se permiten espacios
def test_create_kit_has_spaces_in_name_get_success_response():
    kit_body = get_kit_body(" A Aaa ")
    positive_assert(kit_body)

# Prueba 7: Se permiten números
def test_create_kit_has_numbers_in_name_get_success_response():
    kit_body = get_kit_body("123")
    positive_assert(kit_body)

# Prueba 8: El parámetro no se pasa en la solicitud
def test_create_kit_no_first_name_get_error_response():
    kit_body = {}
    negative_assert_code_400(kit_body)

# Prueba 9: Se ha pasado un tipo de parámetro diferente (número)
def test_create_kit_numeric_type_name_get_error_response():
    kit_body = {"name": 123}
    negative_assert_code_400(kit_body)

# Funciones de aserción (positivas y negativas)
def positive_assert(kit_body):
    auth_token = get_new_user_token()
    response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]

def negative_assert_code_400(kit_body):
    auth_token = get_new_user_token()
    response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert response.status_code == 400