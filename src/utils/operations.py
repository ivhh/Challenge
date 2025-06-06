from collections import defaultdict
import json
import datetime
from typing import Callable, Dict, List, Tuple
import heapq
import itertools

_counter = itertools.count()


def top_elements_heap(element: dict, incremental_field: str, heap: list = None, num_elements=10):
    if heap is None:
        heap = []
    entry = (element[incremental_field], next(_counter), element)
    if len(heap) < num_elements:
        heapq.heappush(heap, entry)
    else:
        if entry[0] > heap[0][0]:
            heapq.heappushpop(heap, entry)
    return heap

def top_elements(
    element: dict, incremental_field: str, top_elements_arr: List = [], num_elements=10
) -> List:
    """
    Returns a list of the top elements based on a specified incremental field.

    Args:
        element (dict): The element to be added to the list.
        incremental_field (str): The field used for comparison to determine the top elements.
        top_elements_arr (List, optional): The list of top elements. Defaults to an empty list.
        num_elements (int, optional): The maximum number of elements to keep in the list. Defaults to 10.

    Returns:
        List: The updated list of top elements.
    """
    if len(top_elements_arr) < num_elements:
        # Add element to the list
        top_elements_arr.append(element)
    elif (
        element[incremental_field]
        > top_elements_arr[num_elements - 1][incremental_field]
    ):
        idx = num_elements
        top_elements_arr.append(element)
        remove_last = True
        while (
            idx > 0
            and top_elements_arr[idx - 1][incremental_field]
            < top_elements_arr[idx][incremental_field]
        ):
            # here checks element if exists in the list
            is_equal = True
            for key in element.keys():
                if key == incremental_field:
                    continue
                if top_elements_arr[idx][key] != top_elements_arr[idx - 1][key]:
                    is_equal = False
                    break
            if is_equal:
                top_elements_arr.pop(idx - 1)
                remove_last = False
                idx -= 1
                continue
            aux = top_elements_arr[idx]
            top_elements_arr[idx] = top_elements_arr[idx - 1]
            top_elements_arr[idx - 1] = aux
            idx -= 1
        if remove_last:
            top_elements_arr.pop()
    return top_elements_arr


import datetime


def parse_field(field: str, type: str, data: dict):
    """
    Parses a field from the given data dictionary based on the specified type.

    Args:
        field (str): The name of the field to parse.
        type (str): The type of the field. Valid types are "date", "int", and "string".
        data (dict): The dictionary containing the data.

    Returns:
        The parsed field value based on the specified type.

    Raises:
        ValueError: If the specified type is not valid.
    """
    parsed_data = None
    if type == "date":
        parsed_data = datetime.datetime.strptime(data[field], "%Y-%m-%d").date()
    elif type == "int":
        parsed_data = int(data[field])
    elif type == "str":
        parsed_data = str(data[field])
    else:
        raise ValueError(f"Invalid type: {type}")
    return parsed_data


def get_value(data: dict, field: str, transformations: Dict[str, Callable] = {}):
    """
    Returns the value of a field from the given data dictionary.

    Args:
        data (dict): The dictionary containing the data.
        field (str): The name of the field to retrieve. If the field is nested, use dot notation (e.g., "user.name").

    Returns:
        The value of the specified field from the data dictionary.
    """
    field_tree = field.split(".")
    fetch_data = data
    for f in field_tree:
        fetch_data = fetch_data.get(f)
        if fetch_data is None:
            return None
        if transformations.get(f):
            fetch_data = transformations[f](fetch_data)
    return fetch_data


def aggregate_multiline_json(
    file_path: str,
    fields: List[str],
    return_fields: List[Tuple[str, str]],
    transformations: Dict[str, Callable] = {},
    break_down_field: str = "",
) -> List[Tuple]:
    """
    Aggregate data from a multiline JSON file based on specified fields.

    Args:
        file_path (str): The path to the JSON file.
        fields (List[str]): The fields to extract from each JSON object.
        return_fields (List[Tuple[str, str]]): The fields to include in the output.
        transformations (Dict[str, Callable], optional): Dictionary of transformation functions for each field. Defaults to {}.
        break_down_field (str, optional): The field to break down the aggregation by. Defaults to "".

    Returns:
        List[Tuple]: A list of tuples representing the aggregated data.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        Exception: If any other error occurs during the aggregation process.
    """
    count_map = defaultdict(int)
    output_arr = []
    try:
        with open(file_path, "r") as f:
            for ln, line in enumerate(f):
                try:
                    jdata = json.loads(line)
                except json.JSONDecodeError:
                    print(f"Invalid JSON in line number: {ln}")
                    continue
                data = {}
                valid_data = True
                for field in fields:
                    data[field] = get_value(jdata, field, transformations)
                    if data[field] is None:
                        valid_data = False
                        break
                if not valid_data:
                    # this was intended to be used, but in Q3 data is optional
                    # but i didn't want to add an extra variable to the Tuple
                    # print(f"Invalid data in line number: {ln}")
                    continue
                if break_down_field != "":
                    keys = []
                    for value in data[break_down_field]:
                        key_data = []
                        for field in fields:
                            if field == break_down_field:
                                key_data.append(value)
                            else:
                                key_data.append(data[field])
                        key = tuple(key_data)
                        keys.append(key)
                else:
                    keys = [tuple(data[field] for field in fields)]
                for key in keys:
                    count_map[key] += 1
                    element = {}
                    for f_idx, field in enumerate(fields):
                        if field != break_down_field:
                            element[field] = data[field]
                        else:
                            element[field] = key[f_idx]
                    element["count"] = count_map[key]
                    output_arr = top_elements(
                        element,
                        "count",
                        output_arr,
                    )
            output = []
        for el in output_arr:
            return_data = []
            for field in return_fields:
                field_name, field_type = field
                return_data.append(parse_field(field_name, field_type, el))
            output.append(tuple(return_data))
        return output
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
