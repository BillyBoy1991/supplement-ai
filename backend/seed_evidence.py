"""
Seed de evidence_chunks para el RAG (Fase 2b).

Fragmentos de evidencia ficticios pero plausibles (demo — ver docs/out-of-scope.md).
Cada content se embebe localmente con sentence-transformers en el momento del
seed; si los embeddings no están disponibles (p. ej. sin red para descargar el
modelo la primera vez) se omite el seed sin romper el arranque.
Run inside the backend container: python seed_evidence.py
"""
import logging
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))

from engine.embeddings import get_embedding
from models.db import EvidenceChunk, SessionLocal

logger = logging.getLogger(__name__)

EVIDENCE: dict[str, list[dict]] = {
    "vitamin-d3": [
        {
            "content": (
                "La vitamina D3 actúa como una prohormona que regula la absorción intestinal de calcio "
                "y fósforo. Niveles séricos de 25(OH)D por encima de 30 ng/mL se asocian con mejor "
                "densidad mineral ósea en adultos."
            ),
            "source": "PubMed 2022 · PMID:35418463",
        },
        {
            "content": (
                "Ensayos controlados sugieren que la suplementación con vitamina D en personas con "
                "déficit mejora la función muscular y reduce la fatiga autopercibida. El efecto es "
                "mayor en quienes parten de niveles inferiores a 20 ng/mL."
            ),
            "source": "PubMed 2021 · PMID:33892479",
        },
        {
            "content": (
                "Receptores de vitamina D están presentes en tejido inmune, y su déficit se ha "
                "relacionado con mayor susceptibilidad a infecciones respiratorias. La suplementación "
                "diaria muestra efecto protector modesto frente a dosis altas espaciadas."
            ),
            "source": "PubMed 2023 · PMID:36719842",
        },
    ],
    "magnesium-glycinate": [
        {
            "content": (
                "El magnesio participa como cofactor en más de 300 reacciones enzimáticas, incluida la "
                "regulación del eje GABA-glutamato. La forma glicinato presenta alta biodisponibilidad "
                "y menor efecto laxante que el óxido de magnesio."
            ),
            "source": "PubMed 2022 · PMID:35184264",
        },
        {
            "content": (
                "En adultos con insomnio leve, la suplementación con magnesio se asocia con reducción "
                "de la latencia del sueño y mejora subjetiva de su calidad. El mecanismo propuesto "
                "implica la modulación de receptores NMDA y la secreción de melatonina."
            ),
            "source": "PubMed 2021 · PMID:34883514",
        },
        {
            "content": (
                "Estudios observacionales relacionan ingestas bajas de magnesio con mayor reactividad "
                "al estrés y síntomas de ansiedad leve. Los ensayos de suplementación muestran mejoras "
                "moderadas en escalas de estrés percibido tras 8 semanas."
            ),
            "source": "PubMed 2020 · PMID:32503201",
        },
    ],
    "omega-3": [
        {
            "content": (
                "Los ácidos grasos EPA y DHA se incorporan a las membranas celulares y reducen la "
                "producción de eicosanoides proinflamatorios. Dosis combinadas de 1-2 g/día muestran "
                "reducción consistente de triglicéridos plasmáticos."
            ),
            "source": "PubMed 2022 · PMID:35672384",
        },
        {
            "content": (
                "El DHA es un componente estructural mayoritario de la corteza cerebral y la retina. "
                "Ensayos en adultos mayores sugieren que la suplementación con omega-3 ralentiza el "
                "declive cognitivo leve asociado a la edad."
            ),
            "source": "PubMed 2023 · PMID:36841098",
        },
        {
            "content": (
                "Metaanálisis de ensayos aleatorizados encuentran efecto antidepresivo adyuvante "
                "pequeño pero significativo para formulaciones ricas en EPA (>60% del total), no así "
                "para las dominadas por DHA."
            ),
            "source": "PubMed 2021 · PMID:34216046",
        },
    ],
    "vitamin-b12": [
        {
            "content": (
                "La vitamina B12 es esencial para la síntesis de mielina y la maduración de glóbulos "
                "rojos. Su déficit cursa con fatiga, parestesias y anemia megaloblástica, y es "
                "frecuente en dietas veganas no suplementadas."
            ),
            "source": "PubMed 2022 · PMID:35291842",
        },
        {
            "content": (
                "En adultos con niveles séricos bajos de B12, la suplementación oral con cianocobalamina "
                "o metilcobalamina normaliza marcadores hematológicos en 8-12 semanas. La vía oral en "
                "dosis altas es tan eficaz como la intramuscular en la mayoría de casos."
            ),
            "source": "PubMed 2020 · PMID:32108559",
        },
    ],
    "ashwagandha": [
        {
            "content": (
                "Los witanólidos de Withania somnifera modulan el eje hipotálamo-hipófisis-adrenal. "
                "Ensayos aleatorizados con extracto de raíz (300-600 mg/día) muestran reducciones "
                "significativas de cortisol sérico y estrés percibido frente a placebo."
            ),
            "source": "PubMed 2021 · PMID:34254920",
        },
        {
            "content": (
                "En adultos con insomnio no orgánico, la ashwagandha mejora la eficiencia del sueño y "
                "reduce la latencia de inicio medida por actigrafía. Los efectos aparecen de forma "
                "consistente a partir de las 8 semanas de uso."
            ),
            "source": "PubMed 2022 · PMID:35509723",
        },
        {
            "content": (
                "Revisiones sistemáticas señalan mejoras moderadas en fuerza y recuperación muscular "
                "con extracto de ashwagandha en adultos que entrenan, posiblemente vía atenuación del "
                "daño muscular inducido por cortisol."
            ),
            "source": "PubMed 2023 · PMID:36705108",
        },
    ],
    "rhodiola-rosea": [
        {
            "content": (
                "La Rhodiola rosea actúa como adaptógeno modulando la liberación de cortisol y la "
                "actividad de la beta-endorfina. Ensayos en personas con fatiga relacionada con estrés "
                "muestran mejoras en síntomas de agotamiento desde la primera semana."
            ),
            "source": "PubMed 2021 · PMID:34055219",
        },
        {
            "content": (
                "Los principios activos rosavinas y salidrósido atraviesan la barrera hematoencefálica "
                "e influyen en la neurotransmisión monoaminérgica. Estudios piloto reportan mejoras en "
                "atención sostenida y rendimiento mental bajo fatiga."
            ),
            "source": "PubMed 2022 · PMID:35628472",
        },
    ],
    "creatine": [
        {
            "content": (
                "La creatina monohidrato aumenta las reservas de fosfocreatina muscular, mejorando la "
                "resíntesis de ATP en esfuerzos de alta intensidad. Es uno de los suplementos con mayor "
                "respaldo de evidencia para fuerza y potencia."
            ),
            "source": "PubMed 2021 · PMID:34234088",
        },
        {
            "content": (
                "Más allá del músculo, el cerebro también almacena fosfocreatina. Ensayos en adultos "
                "con privación de sueño o alta demanda cognitiva sugieren beneficios leves de la "
                "creatina sobre memoria de trabajo y velocidad de procesamiento."
            ),
            "source": "PubMed 2023 · PMID:36893011",
        },
        {
            "content": (
                "Dosis de mantenimiento de 3-5 g/día son seguras a largo plazo en adultos sanos según "
                "revisiones de seguridad, sin evidencia de daño renal en población sin patología previa."
            ),
            "source": "PubMed 2020 · PMID:32305824",
        },
    ],
    "melatonin": [
        {
            "content": (
                "La melatonina exógena adelanta la fase circadiana y reduce la latencia de inicio del "
                "sueño, con efecto más marcado en trastornos del ritmo circadiano y jet lag. Dosis "
                "bajas (0.5-2 mg) tomadas 1-2 horas antes de acostarse son suficientes."
            ),
            "source": "PubMed 2022 · PMID:35442882",
        },
        {
            "content": (
                "Metaanálisis en insomnio primario muestran que la melatonina reduce la latencia del "
                "sueño en torno a 7 minutos y aumenta modestamente el tiempo total de sueño, con un "
                "perfil de efectos adversos comparable a placebo a corto plazo."
            ),
            "source": "PubMed 2021 · PMID:33987339",
        },
    ],
    "l-theanine": [
        {
            "content": (
                "La L-teanina cruza la barrera hematoencefálica y aumenta la actividad de ondas alfa "
                "cerebrales, asociadas a un estado de relajación alerta. Dosis de 200 mg reducen "
                "marcadores fisiológicos de respuesta al estrés agudo."
            ),
            "source": "PubMed 2020 · PMID:31758301",
        },
        {
            "content": (
                "En combinación con cafeína, la L-teanina mejora la atención sostenida y reduce la "
                "irritabilidad asociada a la cafeína sola. Sola, muestra efectos ansiolíticos leves "
                "sin sedación ni deterioro psicomotor."
            ),
            "source": "PubMed 2021 · PMID:34619298",
        },
    ],
    "probiotics": [
        {
            "content": (
                "Cepas de Lactobacillus y Bifidobacterium restauran la diversidad de la microbiota "
                "tras disbiosis, reforzando la barrera intestinal y la producción de ácidos grasos de "
                "cadena corta. El efecto es cepa-específico y dependiente de dosis (≥10^9 UFC/día)."
            ),
            "source": "PubMed 2022 · PMID:35730561",
        },
        {
            "content": (
                "Metaanálisis en síndrome de intestino irritable muestran mejoras en hinchazón y "
                "malestar abdominal con probióticos multicepa frente a placebo, con heterogeneidad "
                "alta entre formulaciones."
            ),
            "source": "PubMed 2021 · PMID:34121542",
        },
        {
            "content": (
                "El eje intestino-cerebro media efectos de ciertos psicobióticos sobre el estado de "
                "ánimo: ensayos con Lactobacillus helveticus y Bifidobacterium longum reportan "
                "reducciones leves de ansiedad y cortisol urinario."
            ),
            "source": "PubMed 2023 · PMID:36952411",
        },
    ],
}


def seed_evidence(db) -> None:
    """Inserta los chunks de evidencia con su embedding. Idempotente por slug."""
    try:
        get_embedding("ping")
    except Exception as exc:
        logger.warning("Embeddings no disponibles, se omite el seed de evidencia: %s", exc)
        print(f"Evidence seed skipped (embeddings unavailable): {exc}")
        return

    inserted = 0
    skipped = 0
    for slug, chunks in EVIDENCE.items():
        exists = db.query(EvidenceChunk).filter(EvidenceChunk.supplement_slug == slug).first()
        if exists:
            skipped += 1
            continue
        for chunk in chunks:
            db.add(EvidenceChunk(
                id=uuid.uuid4(),
                supplement_slug=slug,
                content=chunk["content"],
                embedding=get_embedding(chunk["content"]),
                source=chunk["source"],
            ))
            inserted += 1
    db.commit()
    print(f"Evidence seed complete: {inserted} chunks inserted, {skipped} slugs already seeded.")


def main() -> None:
    db = SessionLocal()
    try:
        seed_evidence(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
