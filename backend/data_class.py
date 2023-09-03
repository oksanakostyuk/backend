from typing import Dict, Any, List, Tuple
import pandas as pd


# - **UNIFORMITY** Is the data in the same format (per column)?
# - **DUPLICATES** Are no duplicates in the data?
# - **MISSING VALUES** Are there any null / missing values?
# - **OUTLIERS** Any outliers in the data (per column)?




column_name = str


class DataClass:
    def __init__(self, path: str, separator: str = ",") -> None:
        self.df: pd.DataFrame = pd.read_csv(path, sep=separator)

    def check_uniformity(self) -> Dict[column_name, List[int]]:
        # Return a dict mapping column name to a list of row indexes which are not uniform

        return {}

    def check_duplicates(self) -> List[Tuple[int]]:
        """Check for duplicate rows in the data.

        Here I am joining self.df to itself on all the columns, this way the duplicating rows
        will be the ones where indices don't match. According to the test, first index has to
        be lower than the second one, thus the filtering condition. The rest is formatting.

        Returns:
            List[Tuple[int]]: list of tuples of row indexes where each tuple represents a 
            duplicate group
        """
        join_data = self.df.copy()
        join_data['index'] = self.df.index
        merged = join_data.merge(join_data, on=list(self.df.columns), suffixes=('_l', '_r'))
        # this condition is based on the test
        pairs = merged.loc[merged['index_l'] < merged['index_r']]
        # formatting to get the list of tuples
        return list(pairs[['index_l', 'index_r']].itertuples(index=False, name=None))

    def check_missing_values(self) -> List[int]:
        """Check missing values and empty strings in the dataset.

        Returns:
            List[int]: row indexes which contain empty values
        """
        return list(self.df.loc[
            # check all nas + check for empty strings
            self.df.isna().add(self.df.values == '').sum(axis = 1) >= 1
            ].index)

    def check_outliers(self) -> Dict[column_name, List[int]]:
        """Check dataset for outliers using 1.5 IQR method.

        Method: https://towardsdatascience.com/why-1-5-in-iqr-method-of-outlier-detection-5d07fdc82097

        Returns:
            Dict[column_name, List[int]]: mapping column name to a list of row indexes which are outliers
        """
        # calculate quartiles
        Q3 = self.df.quantile(0.75, numeric_only=True)
        Q1 = self.df.quantile(0.25, numeric_only=True)
        
        # calculate respective boundaries
        lower = Q1 - 1.5*(Q3-Q1)
        upper = Q3 + 1.5*(Q3-Q1)
        
        # construct outliers dictionary
        outliers = {}
        for column_name in lower.index:
            outliers[column_name] = \
                list(self.df.loc[self.df[column_name] < lower[column_name]].index) \
                + \
                list(self.df.loc[self.df[column_name] > upper[column_name]].index)

        return outliers

    def generate_report(self) -> Dict[str, Any]:
        report = {
            "UNIFORMITY": self.check_uniformity(),
            "DUPLICATE_ROWS": self.check_duplicates(),
            "MISSING_VALUE_ROWS": self.check_missing_values(),
            "OUTLIERS": self.check_outliers(),
        }
        return report
