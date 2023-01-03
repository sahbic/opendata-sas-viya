def save_and_format_date(df, date_column, s, output_name, temp_name, caslib):
    s.droptable(name=output_name, caslib=caslib, quiet=True)
    castbl = s.upload_frame(df, casout={"name":output_name, "caslib":caslib, "promote":True})

    s.dropTable(name=temp_name, caslib=caslib, quiet=True)
    res = s.dataStep.runCode(
        code='''data {0}.{1}(promote=yes);
                set {0}.{2};
                FORMAT sas_date YYMMDD10.;
                sas_date=input({3}, ANYDTDTE10.);
                run;'''.format(caslib, temp_name, output_name, date_column))

    s.dropTable(name=output_name, caslib=caslib, quiet=True)
    res = s.alterTable(temp_name,
                    rename=output_name,
                    caslib=caslib,
                    columns=[{"name":date_column, "drop":True},
                            {"name":"sas_date", "rename":date_column}
                           ]
                    )
    # save table
    res = s.save(table={"name":output_name, "caslib":caslib}, name=output_name+".sashdat", caslib=caslib, replace=True)
    
def upload_save_table(df, s, output_name, caslib):
    # drop table
    s.droptable(name=output_name, caslib=caslib, quiet=True)
    # upload table
    castbl = s.upload_frame(df, casout={"name":output_name, "caslib":caslib, "promote":True})
    # save table
    res = s.save(table={"name":output_name, "caslib":caslib}, name=output_name+".sashdat", caslib=caslib, replace=True)