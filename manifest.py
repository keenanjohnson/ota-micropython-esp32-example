import datetime
import subprocess
import os

include("$(MPY_DIR)/extmod/asyncio")
freeze("$(PORT_DIR)/modules")
require("ntptime")
require("ssl")
freeze("src")

# version = subprocess.check_output(
#     [
#         "git",
#         "describe",
#         "--tags",  # Necessary because `actions/checkout` doesn't keep the annotated tags for some reason https://github.com/actions/checkout/issues/290
#     ],
#     encoding="utf-8",
# )

version = "0.0.1"

commit_id = subprocess.check_output(
    ["git", "rev-parse", "HEAD"],
    encoding="utf-8",
)

if "SOURCE_DATE_EPOCH" in os.environ:
    now = datetime.datetime.utcfromtimestamp(float(os.environ["SOURCE_DATE_EPOCH"]))
else:
    now = datetime.datetime.utcnow()

with open("__version__.py", "w", encoding="utf-8") as f:
    f.write("version = %r\n" % version.strip())
    f.write("commit_id = %r\n" % commit_id.strip())
    f.write("build_date = %r\n" % now.isoformat())
    f.write("build_year = %d\n" % now.year)

    # This is the primary manifest, so write the BETA Tag to False
    f.write("beta = False\n")

os.utime("__version__.py", (now.timestamp(), now.timestamp()))

module("__version__.py")
