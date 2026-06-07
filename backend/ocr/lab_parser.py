import re


class LabParser:

    def extract_lab_values(self, text):

        results = {}

        creatinine = re.search(
            r"creatinine[:\s]*([\d.]+)",
            text.lower()
        )

        alt = re.search(
            r"alt[:\s]*([\d.]+)",
            text.lower()
        )

        ast = re.search(
            r"ast[:\s]*([\d.]+)",
            text.lower()
        )

        if creatinine:
            results["creatinine"] = float(
                creatinine.group(1)
            )

        if alt:
            results["alt"] = float(
                alt.group(1)
            )

        if ast:
            results["ast"] = float(
                ast.group(1)
            )

        return results