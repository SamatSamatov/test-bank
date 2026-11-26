import random
import uuid

import rstr
from typing import Any, get_type_hints, Annotated, get_origin, get_args

from src.main.api.generators.creation_rule import CreationRule


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type, **overrides) -> Any:
        """
          Генерирует экземпляр модели.
          :param cls: класс модели
          :param overrides: поля для явной установки (например, accountId=123)
        """
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            # Если поле передано через overrides — используем его
            if field_name in overrides:
                init_data[field_name] = overrides[field_name]
                continue

            rule = None
            actual_type = annotated_type()

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, CreationRule):
                        rule = ann

            if rule:
                value = RandomModelGenerator._generate_from_rule(rule, actual_type)
            else:
                value = RandomModelGenerator._generate_value(actual_type)

            init_data[field_name] = value

        return cls(**init_data)

    @staticmethod
    def _generate_from_rule(rule: CreationRule, field_type: type) -> Any:
        if rule.choices is not None:
            return random.choice(rule.choices)

        if rule.min_value is not None or rule.max_value is not None:
            min_v = rule.min_value if rule.min_value is not None else 0
            max_v = rule.max_value if rule.max_value is not None else 10000

            if field_type is int:
                return random.randint(int(min_v), int(max_v))
            elif field_type is float:
                return round(random.uniform(min_v, max_v), 2)

        if rule.regex:
            generated = rstr.xeger(rule.regex)
            if field_type is int:
                return int(generated)
            if field_type is float:
                return float(generated)
            return generated

        return RandomModelGenerator._generate_value(field_type)

    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(1, 9999)
        elif field_type is float:
            return round(random.uniform(0, 100), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is list:
            return [str(uuid.uuid4())[:5]]
        elif isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)
        return None


