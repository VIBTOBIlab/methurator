import rich_click as click


def percentage_checker(percentages):
    """
    Converts a comma-separated string into a list of floats.
    """
    list_percentages = [float(x.strip()) for x in percentages.split(",")]

    if any(p <= 0 or p >= 1 for p in list_percentages):
        raise click.UserError("Percentages must be between 0 and 1 (exclusive).")

    if len(list_percentages) < 4:
        raise click.UserError("At least four percentages must be provided.")
    return list_percentages
