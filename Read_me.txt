Code developed by Florian MAVOLLE, Mathias BAUDRY, ALICIA PEREIRA RIBEIRO.

You will find 4 direcroties:
- Class: all the classes that are used to perform the backtest.
- Test: tests that allow to check the classes.
- Data: input data for the market variables (spot, rate, div, ...) and the smile.
- Reports: output from the backtest.
    - opt: one report for each option with its life cycle
    - positions: one report for each date with the all the options
    - delta_hege: one global report for the delta hedging of the whole book

You can run the first book and second book on the corresponding python file, it will generate the Reports automatically.
For the second book, BE CAREFUL:
    - You must choose either you want to backtest with ou without smile. Set Second_book.py -> line 24:Sml=True or False
    - If you choose with smile and that you want to price the replication option long (K1) with the volatility
        of the option short (K2) as explained in the report:
        BinaryOption.py -> Method: Setter -> Comment Line 339/340 and Uncomment Line 341/342.
        Do the other way around if you want to price the replication option normally.

Finally, there is also the Notebook that helped us to retrieve Data from deribit.

