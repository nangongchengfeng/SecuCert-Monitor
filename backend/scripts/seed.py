import sys
import os
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import BaseProvider

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models import ExpirationMonitor

fake = Faker('zh_CN')


class CertificateProvider(BaseProvider):
    def service_name(self):
        domains = ['example.com', 'test.com', 'api.example.cn', 'app.test.net',
                   'web.service.com', 'gateway.api.cn', 'auth.example.com',
                   'cdn.service.net', 'mail.example.cn', 'cloud.test.com']
        return f"{self.random_element(domains)}"

    def department(self):
        departments = ['产品发展本部', '技术平台本部', '运营管理部', '市场部',
                       '人力资源部', '财务部', '法务部', '研发一部', '研发二部']
        return self.random_element(departments)

    def product(self):
        products = ['企业管理系统', '电商平台', '移动应用', '数据分析平台',
                    'API网关', '用户中心', '支付系统', '物流管理系统']
        return self.random_element(products)

    def organ(self):
        organs = ['天威诚信', 'VeriSign', 'GeoTrust', 'GlobalSign',
                  'DigiCert', 'Symantec', 'Comodo', 'Let\'s Encrypt']
        return self.random_element(organs)

    def person(self):
        return fake.name()

    def cert_type(self):
        types = ['证书', '合同', '服务协议', 'License', '授权书']
        return self.random_element(types)


fake.add_provider(CertificateProvider)


def generate_certificates(count=50):
    app = create_app()

    with app.app_context():
        ExpirationMonitor.query.delete()
        db.session.commit()

        certificates = []
        for i in range(count):
            today = datetime.now()

            random_days = fake.random_int(min=-100, max=700)
            expiration_date = today + timedelta(days=random_days)
            issuance_date = expiration_date - timedelta(days=fake.random_int(min=365, max=730))

            cert = ExpirationMonitor(
                service_name=fake.service_name(),
                use_deploy=fake.department(),
                deployA=fake.department(),
                deployB=fake.department(),
                product=fake.product(),
                scene=fake.text(max_nb_chars=200),
                organ=fake.organ(),
                manage=fake.cert_type(),
                manage_id=f"{fake.year()}SZ-L-K-{fake.random_number(digits=4)}",
                issuance_date=issuance_date,
                expiration_date=expiration_date,
                header=fake.person(),
                tech=fake.person(),
                yumwei=f"{fake.person()}、{fake.person()}",
                yumwei_time=fake.random_element(['每月/次', '每季度/次', '每半年/次', '每年/次']),
                manager=f"{fake.person()}、{fake.person()}",
                type=fake.cert_type(),
                remark=fake.sentence() if fake.boolean(chance_of_getting_true=50) else None
            )
            certificates.append(cert)

        db.session.bulk_save_objects(certificates)
        db.session.commit()

        print(f"成功生成 {count} 条证书数据！")


if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    generate_certificates(count)
