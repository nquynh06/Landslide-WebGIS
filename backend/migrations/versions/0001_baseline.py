"""Backend and spatial catalog baseline."""

from pathlib import Path

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Immutable revision-local snapshot; later schema.sql revisions cannot change it.
    sql = Path(__file__).with_suffix(".sql").read_text(encoding="utf-8")
    op.execute(sql.strip())


def downgrade():
    for table in (
        "alert_rainfall_records", "gis_layer_study_areas", "alerts", "rainfall_records",
        "landslide_events", "susceptibility_maps", "rubric_criteria", "gis_layers",
        "data_sources", "study_areas",
    ):
        op.drop_table(table)
