import unittest
import minio_util
class MyTestCase(unittest.TestCase):
    def test_something(self):
        # self.assertEqual(True, False)  # add assertion here
        minio_obj = minio_util.Bucket(service="minio.dev.tdaas.phadata.net", access_key="admin", secret_key="12345678")
        minio_obj.fput_file("test", "jiegeyyds.pdf", "/Users/linx/Downloads/20210918.xlsx")


if __name__ == '__main__':
    unittest.main()
