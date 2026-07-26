from packages.retrieval.models import QueryEntities

class FilterBuilder:

    def build(self, entities: QueryEntities) -> dict | None:
        filters = []

        if entities.cve_id:
            filters.append({
                "cve_id": {"$eq": entities.cve_id}
            })

        if entities.cwe_ids:
            filters.append({
                "cwe_ids": {"$in": entities.cwe_ids}
            })

        # if entities.severity:
        #     filters.append({
        #         "severity": {"$eq": entities.severity}
        #     })

        # if entities.vendor:
        #     filters.append({
        #         "vendor": {"$eq": entities.vendor}
        #     })

        # if entities.product:
        #     filters.append({
        #         "product": {"$eq": entities.product}
        #     })

        # if entities.attack_vector:
        #     filters.append({
        #         "attack_vector": {"$eq": entities.attack_vector}
        #     })

        # if entities.attack_complexity:
        #     filters.append({
        #         "attack_complexity": {"$eq": entities.attack_complexity}
        #     })

        # if entities.privileges_required:
        #     filters.append({
        #         "privileges_required": {"$eq": entities.privileges_required}
        #     })

        # if entities.published_year:
        #     filters.append({
        #         "published_at": {
        #             "$gte": f"{entities.published_year}-01-01",
        #             "$lte": f"{entities.published_year}-12-31"
        #         }
        #     })

        # if entities.published_after:
        #     filters.append({
        #         "published_year": {"$gt": entities.published_after}
        #     })

        # if entities.cvss_min:
        #     filters.append({
        #         "cvss_score": {"$gte": entities.cvss_min}
        #     })

        # if entities.known_ransomware_use:
        #     filters.append({
        #         "known_ransomware_use": {"$eq": True}
        #     })

        # if entities.required_action:
        #     filters.append({
        #         "required_action": {"$eq": entities.required_action}
        #     })

        # if entities.patch_due_before:
        #     filters.append({
        #         "patch_due_before": {"$lt": entities.patch_due_before}
        #     })

        if not filters:
            return None

        if len(filters) == 1:
            return filters[0]

        return {"$and": filters}