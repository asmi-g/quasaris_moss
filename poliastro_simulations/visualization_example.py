from czml3 import CZML_VERSION, Document, Packet
from czml3.properties import (
    Box,
    BoxDimensions,
    Color,
    Material,
    Position,
    SolidColorMaterial,
)
from czml3.types import Cartesian3Value
packet_box = Packet(
    id="my_id",
    position=Position(cartographicDegrees=[-114.0, 40.0, 300000.0]),
    box=Box(
        dimensions=BoxDimensions(
            cartesian=Cartesian3Value(values=[400000.0, 300000.0, 500000.0])
        ),
        material=Material(
            solidColor=SolidColorMaterial(color=Color(rgba=[0, 0, 255, 255]))
        ),
    ),
)
doc = Document(
    packets=[Packet(id="document", name="box", version=CZML_VERSION), packet_box]
)
print(doc)
with open("box.czml", "w") as f:
    f.write(doc.to_json(indent=2))  # Optional: use indent for readability

