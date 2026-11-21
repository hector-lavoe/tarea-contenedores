import os
import sys
import pandas as pd


def main() -> None:
    input_path = os.getenv("INPUT_PATH", "/data/input/inversiones.csv")
    output_path = os.getenv("OUTPUT_PATH", "/data/output/resumen_inversiones.csv")
    min_investment = float(os.getenv("MIN_INVESTMENT_USD", "0"))

    if not os.path.exists(input_path):
        print(f"[ERROR] No se encontró el archivo de entrada en: {input_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Leyendo datos desde: {input_path}")
    df = pd.read_csv(input_path)
    registros_iniciales = len(df)

    # Limpieza de datos
    df = df.drop_duplicates(subset=["id_operacion"])
    df = df.dropna(subset=["monto_invertido_usd", "valor_actual_usd"])
    df = df[df["monto_invertido_usd"] >= min_investment].copy()

    # Transformación y cálculo de métricas
    df["ganancia_perdida_usd"] = (df["valor_actual_usd"] - df["monto_invertido_usd"]).round(2)
    df["roi_pct"] = ((df["ganancia_perdida_usd"] / df["monto_invertido_usd"]) * 100).round(2)

    resumen = (
        df.groupby(["ticker", "categoria"], as_index=False)
        .agg(
            total_operaciones=("id_operacion", "count"),
            capital_invertido_usd=("monto_invertido_usd", "sum"),
            valor_portafolio_usd=("valor_actual_usd", "sum"),
            ganancia_neta_usd=("ganancia_perdida_usd", "sum"),
            roi_promedio_pct=("roi_pct", "mean"),
        )
        .round(2)
        .sort_values(by="ganancia_neta_usd", ascending=False)
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    resumen.to_csv(output_path, index=False)

    print(f"[INFO] Registros iniciales: {registros_iniciales} | Registros válidos procesados: {len(df)}")
    print(f"[INFO] Resumen exportado exitosamente en: {output_path}")
    print("\n--- Vista previa del resumen generado ---")
    print(resumen.to_string(index=False))


if __name__ == "__main__":
    main()
