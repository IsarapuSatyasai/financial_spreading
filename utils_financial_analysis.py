import re


def generate_final_response(_dir):
    """
    Generates the final response by combining credit lens responses and annual report responses.

    Args:
        _dir (dict): A dictionary containing 'credit_lens_chain_responses' and 'annual_report_chain_responses'.

    Returns:
        dict: A dictionary with keys ordered as specified in 'key_order'. If 'annual_report_chain_responses' is None,
              returns 'credit_lens_chain_responses'. Otherwise, combines both responses, prioritizing 'credit_lens_chain_responses'
              where available.
    """
    key_order = [
        "General",
        "Key figures",
        "Profitability",
        "Profitability (additional insights from the annual report)",
        "Liquidity / Cash Flow",
        "Liquidity / Cash Flow (additional insights from the annual report)",
        "Solvency",
        "Solvency (additional insights from the annual report)",
    ]

    credit_lens_responses = _dir["credit_lens_chain_responses"]
    annual_report_responses = _dir["additional_report_chain_responses"]

    if annual_report_responses is None:
        final_response = credit_lens_responses
    else:
        final_response = {
            key: credit_lens_responses.get(key, annual_report_responses.get(key))
            for key in key_order
        }

    return final_response


def clean_conversion_block(contexts):
    """
    Cleans up 'Conversion Rate' blocks from a list of context dictionaries.

    Each context is expected to be a dictionary with a 'text' key.
    If the text contains the phrase 'Conversion Rate', this function removes
    the entire block starting from 'Conversion Rate' followed by any number
    of decimal numbers (e.g., 0.56818), up to the next non-numeric, non-whitespace character.

    Parameters:
        contexts (list of dict): A list of dictionaries, each containing a 'text' field.

    Returns:
        list of dict: The modified list with 'Conversion Rate' blocks removed where applicable.
    """
    cleaned_contexts = []

    for context in contexts:
        text = context["text"]

        # Check if 'Conversion Rate' is in the text
        if "Conversion Rate" in text:
            # Regex pattern to match 'Conversion Rate' followed by optional decimal numbers
            pattern = r"Conversion Rate\s*(?:\d+\.\d+\s*)*?(?=[^\s\d.]|$)"
            # Remove the matched pattern from the text
            result = re.sub(pattern, "", text, flags=re.DOTALL)
            context["text"] = result

        # Add the cleaned or unchanged context to the result list
        cleaned_contexts.append(context)

    return cleaned_contexts


def remove_currency_block(contexts):
    """
    Removes blocks of text starting with the line "Currency" and ending just before a line starting with "Restated"
    from the "text" field of each dictionary in the input list.

    Args:
        contexts (list of dict): A list of dictionaries, each containing a "text" key with a string value.

    Returns:
        list of dict: A list of dictionaries with the "Currency" blocks removed from the "text" field.
    """

    cleaned_contexts = []

    for context in contexts:
        text = context["text"]

        lines = text.split("\n")
        output_lines = []
        skip = False

        for line in lines:
            if line.strip().startswith("Currency"):
                skip = True
            elif line.strip().startswith("Restated"):
                skip = False
                output_lines.append(line)
            elif not skip:
                output_lines.append(line)

            context["text"] = "\n".join(output_lines)

        cleaned_contexts.append(context)

    return cleaned_contexts
