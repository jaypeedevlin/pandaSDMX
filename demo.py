import pandasdmx
import os       
from pandasdmx import Request, tests
pkg_path = tests.__path__[0]
estat = Request('ESTAT')
filepath = os.path.join(pkg_path, 'data/exr/ecb_exr_ng/generic/ecb_exr_ng_ts.xml')
resp = estat.get(from_file = filepath)
data = resp.msg.data
df, a = resp.write(data, with_attrib = False, asframe = True)