def model(dbt, session):
    raw_df = dbt.source('std', 'title.akas').df()
    names = raw_df[['titleId', 'title']]
    names.rename({'titleId': 'video_id', 'title': 'name'}, inplace=True)
    names.drop_duplicates(inplace=True, ignore_index=True)

    names.reset_index(drop=True, inplace=True)
    names.insert(0, 'id', names.index)
    names['id'] = names['id'].astype('str')

    return names


# This part is user provided model code
# you will need to copy the next section to run the code
# COMMAND ----------
# this part is dbt logic for get ref work, do not modify

def ref(*args, **kwargs):
    refs = {}
    key = '.'.join(args)
    version = kwargs.get("v") or kwargs.get("version")
    if version:
        key += f".v{version}"
    dbt_load_df_function = kwargs.get("dbt_load_df_function")
    return dbt_load_df_function(refs[key])


def source(*args, dbt_load_df_function):
    sources = {"std.title.akas": "read_csv_auto(\u0027data/title.akas.tsv.gz\u0027, sample_size=-1, quote=\"\\t\")"}
    key = '.'.join(args)
    return dbt_load_df_function(sources[key])


config_dict = {}


class config:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get(key, default=None):
        return config_dict.get(key, default)

class this:
    """dbt.this() or dbt.this.identifier"""
    database = "imdb"
    schema = "main"
    identifier = "std_movie_video_alternative_names"
    
    def __repr__(self):
        return '"imdb"."main"."std_movie_video_alternative_names"'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args, **kwargs: ref(*args, **kwargs, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = False

# COMMAND ----------


