import rich_click as click


def percentage_checker(percentages):
    """
    Converts a comma-separated string into a list of floats.
    """
    list_percentages = [float(x.strip()) for x in percentages.split(",")]

    if any(p == 0 for p in list_percentages):
        raise click.UserError("Percentages must be between > 0.")

    if len(list_percentages) < 4:
        raise click.UserError("At least four percentages must be provided.")

    # And now add 1 if not persent to the list
    # to calculate CpG number on original sample
    if 1 not in list_percentages:
        list_percentages = list_percentages + [1]

    return list_percentages
