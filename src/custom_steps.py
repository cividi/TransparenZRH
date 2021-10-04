from frictionless import Plugin, Step, Field
from datetime import datetime

class transparenzrhPlugin(Plugin):
    code = "transparenZRH"
    status = "experimental"

    def create_step(self, descriptor):
        if "code" in descriptor.keys():
            if descriptor["code"] == "date-transform":
                descriptor.pop("code")
                return date_transform_step(**descriptor)
            if descriptor["code"] == "categorise-sensor":
                descriptor.pop("code")
                return categorise_sensor_step(**descriptor)

class date_transform_step(Step):
    """Transform a date string from sourceFormat into targetFormat (strftime formatters)"""

    code = "date-transform"

    def __init__(self, descriptor=None, *, sourceName=None, targetName=None, targetType=None, sourceFormat=None, targetFormat=None):
        self.setinitial("sourceName", sourceName)
        self.setinitial("sourceFormat", sourceFormat)
        self.setinitial("targetName", targetName)
        self.setinitial("targetFormat", targetFormat)
        self.setinitial("targetType", targetType)
        super().__init__(descriptor)

    def transform_resource(self, resource):
        table = resource.to_petl()
        source = self.get("sourceName")
        strptime = self.get("sourceFormat")
        target = self.get("targetName")
        strftime = self.get("targetFormat")
        type = self.get("targetType")
        
        value = lambda row: datetime.strftime(datetime.strptime(row[source], strptime), strftime)

        if target not in resource.schema.fields:
            field = Field(name=target, type=type)
            resource.schema.add_field(field)
            resource.data = table.addfield(target, value=value)
        else:
            resource.data = table.update(target, value)
    
    # Metadata

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["sourceName","targetName","targetFormat"],
        "properties": {
            "sourceName": {"type": "string"},
            "sourceFormat": {"type": "string"},
            "targetName": {"type": "string"},
            "targetFormat": {"type": "string"},
            "targetType": {"type": "string", "enum": ["string", "integer", "number"]},
        },
    }

class categorise_sensor_step(Step):
    """Match categories based on a mapping"""

    code = "categorise-sensor"

    def __init__(self, descriptor=None, *, sourceName=None, targetName=None):
        self.setinitial("sourceName", sourceName)
        self.setinitial("targetName", targetName)
        super().__init__(descriptor)

    def transform_resource(self, resource):
        table = resource.to_petl()
        source = self.get("sourceName")
        target = self.get("targetName")
        
        value = lambda row: "FUSS" if row[source][:3] == "FZS" else "VELO"

        if target not in resource.schema.fields:
            field = Field(name=target, type="string")
            resource.schema.add_field(field)
            resource.data = table.addfield(target, value=value)
        else:
            resource.data = table.update(target, value)
    
    # Metadata

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["sourceName","targetName"],
        "properties": {
            "sourceName": {"type": "string"},
            "targetName": {"type": "string"},
        },
    }