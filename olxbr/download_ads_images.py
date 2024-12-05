import boto3
from hashlib import md5
import psycopg
from botocore.config import Config
from botocore.exceptions import ClientError


def get_image_urls() -> list[str]:
    with psycopg.connect("postgresql://master:EidZU=>7Q<bcoCKmZQHk>7vhRh+2g75>h9u3wb=J@db.listings-ro.listings-management.private.prod.grupozap.io:5432/listings") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            select image->'imageUrl'
from listing
cross join jsonb_array_elements(images) as e(image)
where id in (2740259471,2685407434,2754864803,2687243752,2754966617,2733232160,2750374077,2710836211,
             2590106695,2652657985,2652646028,2724649290,2736535928,2582733752,2754907417,2740259470,2736535930
    )""")
            return [url[0] for url in cur.fetchall()]


_config: Config = Config(
    region_name="us-east-1",
    connect_timeout=3,
    read_timeout=15
)


def get_s3_file(bucket_name: str, file_name: str, image_file: str) -> bool:
    try:
        s3 = boto3.client('s3', config=_config)
        s3.download_file(bucket_name, file_name, image_file)
    except ClientError as e:
        return False
    return True


def main():
    images = get_image_urls()
    for image in images:
        md5_code = md5(image.encode()).hexdigest()
        image_file_on_s3 = md5_code + ".jpg"
        image_file_on_directory = f"/Users/bparolini/Downloads/imagens/{md5_code}.jpg"

        if not get_s3_file("vr-prod-listings-downloader-images", image_file_on_s3, image_file_on_directory):
            image_file_on_s3 = md5_code + ".webp"
            image_file_on_directory = f"/Users/bparolini/Downloads/imagens/{md5_code}.webp"

            get_s3_file("vr-prod-listings-downloader-images", image_file_on_s3, image_file_on_directory)


if __name__ == "__main__":
    main()
