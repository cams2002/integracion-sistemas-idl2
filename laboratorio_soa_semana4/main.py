import json

from pydantic import ValidationError

from services.claim_transformer import ClaimTransformerService


def main():
    print("=== Transformación XML (Legacy) -> JSON para embeddings de IA ===\n")

    with open("data/sample_claim.xml", "r", encoding="utf-8") as archivo:
        xml_content = archivo.read()

    print("XML de entrada:")
    print(xml_content)

    try:
        resultado = ClaimTransformerService.process_xml_to_ai_json(xml_content)
        print("JSON generado:")
        print(json.dumps(resultado, indent=4, ensure_ascii=False))
    except ValidationError as e:
        print("Error de validación (Pydantic):")
        print(e)
    except ValueError as e:
        print(e)

    # Prueba de validación: póliza sin el prefijo "POL-"
    print("\n=== Prueba de validación: póliza inválida ===")
    xml_invalido = xml_content.replace("POL-9928341", "9928341")
    try:
        ClaimTransformerService.process_xml_to_ai_json(xml_invalido)
    except ValidationError as e:
        print("La reclamación fue rechazada:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()