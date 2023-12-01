import sys
import os

from pathlib import Path

from pyspark.sql import SparkSession


def main():
    if len(sys.argv) != 2:
        print("Usage: main.py <root_path>", file=sys.stderr)
        sys.exit(1)

    root_path = Path(sys.argv[1])

    spark = SparkSession.builder.appName("popularityBasedOnAge").getOrCreate()

    users_age = \
        (spark
         .read.csv(os.path.join(root_path, 'user_age.csv'), header=True, inferSchema=True)
         .cache())
    session_yoga = \
        (spark
         .read.csv(os.path.join(root_path, 'session_yoga.csv'), header=True, inferSchema=True)
         .drop('time')
         .cache())
    session_pilates = \
        (spark
         .read.csv(os.path.join(root_path, 'session_Pilates.csv'), header=True, inferSchema=True)
         .drop('time')
         .cache())
    session_spinning = \
        (spark
         .read.csv(os.path.join(root_path, 'session_Spinning.csv'), header=True, inferSchema=True)
         .drop('time')
         .cache())

    users_age = users_age.filter((users_age.edad >= 18) & (users_age.edad < 60))

    spinning_by_user = count_by_user(session_spinning, 'spinning')
    pilates_by_user = count_by_user(session_pilates, 'pilates')
    yoga_by_user = count_by_user(session_yoga, 'yoga')

    spinning_by_age = join_and_sum(users_age, spinning_by_user, 'spinning')
    pilates_by_age = join_and_sum(users_age, pilates_by_user, 'pilates')
    yoga_by_age = join_and_sum(users_age, yoga_by_user, 'yoga')

    most_popular_activity = \
        (spinning_by_age
         .join(pilates_by_age, on='edad', how='outer')
         .join(yoga_by_age, on='edad', how='outer')
         .selectExpr('edad',
                     'IF(spinning > pilates AND spinning > yoga, "spinning", '
                     'IF(pilates > spinning AND pilates > yoga, "pilates", "yoga")) AS activity')
         .orderBy('edad'))

    print('Most popular activity by age:')
    most_popular_activity.show()


def count_by_user(df, session):
    return df.groupBy('user').count().withColumnRenamed('count', f'count_{session}')


def join_and_sum(df, count_df, session):
    return (df
            .join(count_df, on='user', how='left')
            .groupBy('edad')
            .sum(f'count_{session}')
            .withColumnRenamed(f'sum(count_{session})', session))


if __name__ == '__main__':
    main()
