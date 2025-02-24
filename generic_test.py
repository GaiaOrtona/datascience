from pandas import DataFrame, merge, concat
from processor import Processor
from RelationalQueryProcessor import RelationalQueryProcessor
from TriplestoreQueryProcessor import TriplestoreQueryProcessor
from queryProcessor import QueryProcessor
from data_model import *


class GenericQueryProcessor:
    def __init__(self):
        self.queryProcessors = []

    def cleanQueryProcessors(self):
        self.queryProcessors = []
        return True

    def addQueryProcessor(self, processor: QueryProcessor):  # workssss
        self.queryProcessors.append(processor)
        return True

    def getAllAnnotations(self) -> list[Annotation]:  # workssss
        result = list()
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getAllAnnotations()

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Annotation(
                    row["annotation_ids"],
                    row["annotation_motivations"],
                    IdentifiableEntity(row["annotation_targets"]),
                    Image(row["annotation_bodies"]),
                )
                result.append(entity)

        return result

    def getAllCanvas(self) -> list[Canvas]:  # braveeeee!!!
        result = list()
        df_graph = DataFrame()
        df_rel = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, TriplestoreQueryProcessor):
                df_graph = processor.getAllCanvases()

        if not df_graph.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, RelationalQueryProcessor):
                    for idx, row in df_graph.iterrows():
                        df_rel = concat(
                            [df_rel, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        )

            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )

            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = Canvas(
                    row["id"], row["label"], row["title"], row["creator_name"]
                )
                result.append(entity)

        return result

    def getAllCollections(self) -> list[Collection]:  # braveeeee!!!
        result = list()
        df_graph = DataFrame()
        df_rel = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, TriplestoreQueryProcessor):
                df_graph = processor.getAllCollections()

        if not df_graph.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, RelationalQueryProcessor):
                    for idx, row in df_graph.iterrows():
                        df_rel = concat(
                            [df_rel, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        )

            df_graph = (
                df_graph.groupby(["id", "label"])["items"].apply(list).reset_index()
            )
            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )

            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = Collection(
                    row["id"],
                    row["label"],
                    row["title"],
                    row["creator_name"],
                    row["items"],
                )
                result.append(entity)

        return result

    def getAllImages(self) -> list[Image]:  # worksss
        result = []
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getAllImages()

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Image(row["image_ids"])
                result.append(entity)

        return result

    def getAllManifests(self) -> list[Manifest]:  # worksss
        result = list()
        df_graph = DataFrame()
        df_rel = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, TriplestoreQueryProcessor):
                df_graph = processor.getAllManifests()

        if not df_graph.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, RelationalQueryProcessor):
                    for idx, row in df_graph.iterrows():
                        df_rel = concat(
                            [df_rel, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        )

            df_graph = (
                df_graph.groupby(["id", "label"])["items"].apply(list).reset_index()
            )
            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )

            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = Manifest(
                    row["id"],
                    row["label"],
                    row["title"],
                    row["creator_name"],
                    row["items"],
                )
                result.append(entity)

        return result

    def getAnnotationsToCanvas(
        self, canvasId: str
    ) -> list[Annotation]:  # is working yeeeee
        result = list()
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getAnnotationsWithTarget(canvasId)

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Annotation(
                    row["annotation_ids"],
                    row["annotation_motivations"],
                    IdentifiableEntity(row["annotation_targets"]),
                    Image(row["annotation_bodies"]),
                )
                result.append(entity)

        return result

    def getAnnotationsToCollection(
        self, collectionId: str
    ) -> list[Annotation]:  # it works yeeee
        result = list()
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getAnnotationsWithTarget(collectionId)

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Annotation(
                    row["annotation_ids"],
                    row["annotation_motivations"],
                    IdentifiableEntity(row["annotation_targets"]),
                    Image(row["annotation_bodies"]),
                )
                result.append(entity)

        return result

    def getAnnotationsToManifest(
        self, manifestId: str
    ) -> list[Annotation]:  # it worksss oleeee
        result = list()
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getAnnotationsWithTarget(manifestId)

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Annotation(
                    row["annotation_ids"],
                    row["annotation_motivations"],
                    IdentifiableEntity(row["annotation_targets"]),
                    Image(row["annotation_bodies"]),
                )
                result.append(entity)

        return result

    def getAnnotationsWithBody(
        self, bodyId
    ) -> list[Annotation]:  # it worksss bravissime
        result = []
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getAnnotationsWithBody(bodyId)

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Annotation(
                    row["annotation_ids"],
                    row["annotation_motivations"],
                    IdentifiableEntity(row["annotation_targets"]),
                    Image(row["annotation_bodies"]),
                )
                result.append(entity)

        return result

    def getAnnotationsWithBodyAndTarget(
        self, bodyId: str, targetId: str
    ) -> list[Annotation]:  # worksssss
        result = []
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getAnnotationsWithBodyAndTarget(bodyId, targetId)

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Annotation(
                    row["annotation_ids"],
                    row["annotation_motivations"],
                    IdentifiableEntity(row["annotation_targets"]),
                    Image(row["annotation_bodies"]),
                )
                result.append(entity)

        return result

    def getAnnotationsWithTarget(self, targetId: str) -> list[Annotation]:  # workssss
        result = []
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getAnnotationsWithTarget(targetId)

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Annotation(
                    row["annotation_ids"],
                    row["annotation_motivations"],
                    IdentifiableEntity(row["annotation_targets"]),
                    Image(row["annotation_bodies"]),
                )
                result.append(entity)

        return result

    def getCanvasesInCollection(self, collectionId: str) -> list[Canvas]:  # workssss
        result = list()
        df_graph = DataFrame()
        df_rel = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, TriplestoreQueryProcessor):
                df_graph = processor.getCanvasesInCollection(
                    collectionId
                ).drop_duplicates()

        if not df_graph.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, RelationalQueryProcessor):
                    for idx, row in df_graph.iterrows():
                        df_rel = concat(
                            [df_rel, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        ).drop_duplicates()

            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )
            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = Canvas(
                    row["id"], row["label"], row["title"], row["creator_name"]
                )
                result.append(entity)

        return result

    def getCanvasesInManifest(self, manifestId: str) -> list[Canvas]:  # worksss
        result = list()
        df_graph = DataFrame()
        df_rel = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, TriplestoreQueryProcessor):
                df_graph = processor.getCanvasesInManifest(manifestId)

        if not df_graph.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, RelationalQueryProcessor):
                    for idx, row in df_graph.iterrows():
                        df_rel = concat(
                            [df_rel, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        )

            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )

            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = Canvas(
                    row["id"], row["label"], row["title"], row["creator_name"]
                )
                result.append(entity)

        return result

    def getEntityById(
        self, entityId: str
    ) -> IdentifiableEntity or None:  # workkss oleee
        df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, TriplestoreQueryProcessor) or isinstance(
                processor, RelationalQueryProcessor
            ):
                df = concat([df, processor.getEntityById(entityId)], ignore_index=True)
                df.drop_duplicates()
                for idx, row in df.iterrows():
                    if row["id"]:
                        entity = IdentifiableEntity(row["id"])
                        return entity
                    else:
                        return None

    def getEntitiesWithCreator(
        self, creatorName: str
    ) -> list[EntityWithMetadata]:  # bugs to fix - creators lists
        result = list()
        df_rel = DataFrame()
        df_graph = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getEntitiesWithCreator(creatorName)

        if not df_rel.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, TriplestoreQueryProcessor):
                    for idx, row in df_rel.iterrows():
                        df_graph = concat(
                            [df_graph, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        )

            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )

            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = EntityWithMetadata(
                    row["id"], row["label"], row["title"], row["creator_name"]
                )
                result.append(entity)

        return result

    def getEntitiesWithLabel(self, label: str) -> list[EntityWithMetadata]:  # workssss
        result = list()
        df_graph = DataFrame()
        df_rel = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, TriplestoreQueryProcessor):
                df_graph = processor.getEntitiesWithLabel(label)

        if not df_graph.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, RelationalQueryProcessor):
                    for idx, row in df_graph.iterrows():
                        df_rel = concat(
                            [df_rel, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        )

            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )

            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = EntityWithMetadata(
                    row["id"], row["label"], row["title"], row["creator_name"]
                )
                result.append(entity)

        return result

    def getEntitiesWithTitle(
        self, title: str
    ) -> list[EntityWithMetadata]:  # ıt worksss - forza chiara!!! spacchi tutto
        result = list()
        df_graph = DataFrame()
        df_rel = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getEntitiesWithTitle(title).drop_duplicates()

        if not df_rel.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, TriplestoreQueryProcessor):
                    for idx, row in df_rel.iterrows():
                        df_graph = concat(
                            [df_graph, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        ).drop_duplicates()

            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )

            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = EntityWithMetadata(
                    row["id"], row["label"], row["title"], row["creator_name"]
                )
                result.append(entity)

        return result

    def getImagesAnnotatingCanvas(self, canvasId) -> list[Image]:  # worksss
        result = []
        df_rel = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, RelationalQueryProcessor):
                df_rel = processor.getImagesWithTarget(canvasId)

        if not df_rel.empty:
            for idx, row in df_rel.iterrows():
                entity = Image(row["image_ids"])
                result.append(entity)

        return result

    def getManifestsInCollection(
        self, collectionId: str
    ) -> list[Manifest]:  # workinggg
        result = list()
        df_graph = DataFrame()
        df_rel = DataFrame()
        joined_df = DataFrame()

        for processor in self.queryProcessors:
            if isinstance(processor, TriplestoreQueryProcessor):
                df_graph = processor.getManifestsInCollection(
                    collectionId
                ).drop_duplicates()

        if not df_graph.empty:
            for processor in self.queryProcessors:
                if isinstance(processor, RelationalQueryProcessor):
                    for idx, row in df_graph.iterrows():
                        df_rel = concat(
                            [df_rel, processor.getEntityById(row["id"])],
                            ignore_index=True,
                        ).drop_duplicates()

            df_graph = (
                df_graph.groupby(["id", "label"])["items"].apply(list).reset_index()
            )
            df_rel = (
                df_rel.groupby(["id", "title"])["creator_name"]
                .apply(list)
                .reset_index()
            )

            joined_df = df_graph.merge(df_rel, how="left", on="id").fillna("")

            for idx, row in joined_df.iterrows():
                entity = Manifest(
                    row["id"],
                    row["label"],
                    row["title"],
                    row["creator_name"],
                    row["items"],
                )
                # print(entity.__dict__)
                result.append(entity)

        return result
