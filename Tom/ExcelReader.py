import xlrd3 as xlrd


def excelReader(
    filePath: str, 
    sheetIndex: int,
    byName: bool = True
):
    '''Generates the data from an Excel workbook for test iterations

        NB: this function by default expects data columns' variable names to be declared in the first row

        To import the function to where you need it:
            import the function to your test script:
                > from ExcelReader import excelReader

        To use:
            instantiate an excelReader object:
                > yourVarName = excelReader("file path here", sheetindex)  # sheets are 0-indexed
            iterate over the generated rows:
                > for dataRow in yourVarName:
                    localVar = dataRow["columnname"]

        For a datasheet without variable names in the first row:
            instantiate an excelReader object:
                > yourVarName = excelReader("file path here", sheetindex, byName=False)  
            iterate over the generated rows:
                > for dataRow in yourVarName:
                    localVar = dataRow[columnIndex]
    '''

    # Open the workbook to the specified sheet
    dataSheet = xlrd.open_workbook(filePath).sheet_by_index(sheetIndex)

    if byName:
        # Construct a dictionary of the column indexes referenced by variable name
        columnByName = {dataSheet.cell_value(0, c): c for c in range(dataSheet.ncols)}

        # Iterate over data rows
        for rowi in range(1, dataSheet.nrows): # Skip variable name row
            # Yield the variable values for the current row
            yield {name: dataSheet.cell_value(rowi, coli) for name, coli in columnByName.items()}
    else:
        # Iterate over rows and reference columns by index 
        for rowi in range(dataSheet.nrows):
            yield {coli: dataSheet.cell_value(rowi, coli) for coli in range(dataSheet.ncols)}
