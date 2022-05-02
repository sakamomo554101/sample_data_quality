from pyspark.sql import SparkSession, Row
import pydeequ
from pydeequ.analyzers import AnalysisRunner, Size, Completeness, AnalyzerContext
from pydeequ.suggestions import *
from pydeequ.checks import *
from pydeequ.verification import *
from pydeequ.profiles import *


def main():
    print("start to execute script..")

    spark = (
        SparkSession.builder.config("spark.jars.packages", pydeequ.deequ_maven_coord)
        .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
        .getOrCreate()
    )
    print(f"spark version is {spark.sparkContext.version}")

    df = spark.sparkContext.parallelize(
        [Row(a="foo", b=1, c=5), Row(a="bar", b=2, c=6), Row(a="baz", b=3, c=None)]
    ).toDF()

    # analyze
    print("start to analyze..")
    analysisResult = (
        AnalysisRunner(spark)
        .onData(df)
        .addAnalyzer(Size())
        .addAnalyzer(Completeness("b"))
        .run()
    )

    analysisResult_df = AnalyzerContext.successMetricsAsDataFrame(spark, analysisResult)
    analysisResult_df.show()

    # profile
    print("start to get profile..")
    result = ColumnProfilerRunner(spark).onData(df).run()

    for col, profile in result.profiles.items():
        print(profile)

    # suggestion
    print("start to suggest..")
    suggestionResult = (
        ConstraintSuggestionRunner(spark).onData(df).addConstraintRule(DEFAULT()).run()
    )

    # Constraint Suggestions in JSON format
    print(suggestionResult)

    # verification
    print("start to verify data..")
    check = Check(spark, CheckLevel.Error, "Integrity checks")
    checkResult = (
        VerificationSuite(spark)
        .onData(df)
        .addCheck(
            check.hasSize(lambda x: x >= 3)
            .hasMin("b", lambda x: x == 0)
            .isComplete("c")
            .isUnique("a")
            .isContainedIn("a", ["foo", "bar", "baz"])
            .isNonNegative("b")
        )
        .run()
    )

    checkResult_df = VerificationResult.checkResultsAsDataFrame(spark, checkResult)
    checkResult_df.show()

    if checkResult.status == "Success":
        print("The data passed the test, everything is fine!")

    else:
        print(
            "We found errors in the data, the following constraints were not satisfied:"
        )

        for check_json in checkResult.checkResults:
            if check_json["constraint_status"] != "Success":
                print(
                    f"\t{check_json['constraint']} failed because: {check_json['constraint_message']}"
                )

    # close spark session
    # print(spark._jvm.SparkSession.getDefaultSession().get().sparkContext().isStopped())
    spark.sparkContext._gateway.shutdown_callback_server()
    spark.stop()

    print("end script")


if __name__ == "__main__":
    main()
