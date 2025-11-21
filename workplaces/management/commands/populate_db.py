from django.core.management.base import BaseCommand
from workplaces.models import Department, Staff, Workplaces
import random


class Command(BaseCommand):
    help = "Populate database with sample data"

    def handle(self, *args, **options):
        # Departments data
        departments_data = [
            {
                "name": "Отдел сборки плат",
                "description": "Отдел занимается сборкой печатных плат",
            },
            {
                "name": "Отдел тестирования",
                "description": "Отдел проводит тестирование продукции",
            },
            {
                "name": "Отдел упаковки",
                "description": "Отдел отвечает за упаковку готовой продукции",
            },
            {
                "name": "Отдел качества",
                "description": "Отдел контролирует качество продукции",
            },
            {
                "name": "Отдел разработки",
                "description": "Отдел разрабатывает новые продукты",
            },
            {
                "name": "Отдел логистики",
                "description": "Отдел управляет логистикой и поставками",
            },
        ]

        # Create departments
        departments = []
        for dep_data in departments_data:
            dep = Department.objects.create(**dep_data)
            departments.append(dep)
        self.stdout.write(self.style.SUCCESS(f"Created {len(departments)} departments"))

        # Staff data
        first_names = [
            "Иван",
            "Петр",
            "Сергей",
            "Алексей",
            "Дмитрий",
            "Андрей",
            "Михаил",
            "Владимир",
            "Николай",
            "Олег",
            "Юрий",
            "Виктор",
            "Анатолий",
            "Геннадий",
            "Валерий",
            "Станислав",
            "Роман",
            "Артем",
            "Кирилл",
            "Максим",
            "Евгений",
            "Денис",
            "Игорь",
            "Вячеслав",
            "Григорий",
            "Тимур",
            "Рустам",
            "Эдуард",
            "Леонид",
            "Борис",
        ]
        last_names = [
            "Иванов",
            "Петров",
            "Сидоров",
            "Кузнецов",
            "Смирнов",
            "Попов",
            "Васильев",
            "Михайлов",
            "Федоров",
            "Соколов",
            "Яковлев",
            "Алексеев",
            "Лебедев",
            "Егоров",
            "Павлов",
            "Семенов",
            "Голубев",
            "Виноградов",
            "Богданов",
            "Воробьев",
            "Фролов",
            "Жуков",
            "Зайцев",
            "Соловьев",
            "Волков",
            "Зуев",
            "Поляков",
            "Ковалев",
            "Романов",
            "Тихонов",
        ]

        staff_count = 0
        for i, dep in enumerate(departments):
            for j in range(5):  # 5 staff per department
                first_name = first_names[(i * 5 + j) % len(first_names)]
                last_name = last_names[(i * 5 + j) % len(last_names)]
                email = f"{first_name.lower()}.{last_name.lower()}@example.com"
                phone = str(random.randint(10000, 99999))
                Staff.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    department=dep,
                    email=email,
                    phone=phone,
                )
                staff_count += 1
        self.stdout.write(self.style.SUCCESS(f"Created {staff_count} staff members"))

        # Workplaces data
        workplaces_data = [
            {
                "name": "Рабочий стол сборщика 1",
                "description": "Рабочий стол для сборки плат",
                "type": "pcplace",
                "department": departments[0],
                "ip": "192.168.1.10",
                "mac": "00:11:22:33:44:54",
            },
            {
                "name": "Ноутбук тестировщика",
                "description": "Ноутбук для тестирования",
                "type": "pcplace",
                "department": departments[1],
                "ip": "192.168.1.11",
                "mac": "00:11:22:33:44:55",
            },
            {
                "name": "Сервер разработки",
                "description": "Сервер для разработки ПО",
                "type": "pcplace",
                "department": departments[2],
                "ip": "192.168.1.12",
                "mac": "00:11:22:33:44:56",
            },
            {
                "name": "Сетевое устройство логистики",
                "description": "Сетевое устройство для логистики",
                "type": "nopcplace",
                "department": departments[3],
                "ip": "",
                "mac": "",
            },
            {
                "name": "Рабочий стол упаковщика",
                "description": "Рабочий стол для упаковки",
                "type": "nopcplace",
                "department": departments[4],
                "ip": "",
                "mac": "",
            },
        ]

        workplaces_count = 0
        for wp_data in workplaces_data:
            Workplaces.objects.create(**wp_data)
            workplaces_count += 1
        self.stdout.write(self.style.SUCCESS(f"Created {workplaces_count} workplaces"))

        # Final report
        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
        self.stdout.write(f"Total Departments: {len(departments)}")
        self.stdout.write(f"Total Staff: {staff_count}")
        self.stdout.write(f"Total Workplaces: {workplaces_count}")
