# F1 Tyre Strategy

This project is Monte Carlo Tyre strategy simulator designed to model and evaluate Formula One strategies under uncertainty. Simulating thousands of race scenios to assess the impact of tyre degradation, pit stop timing, compound selection, and track time position on overal race peformance. 

The goal is to replicate how engineers in F1 would do to discuss the right tyre compound and right pit stop window to change the tyre as a way to support race strategy decision making, rather than relying on determinstic lap-by-lap predictions. 

***Keeping in mind that that weather is not included in the simulator due to the limitation that is not available***

This simulation allows the model to:
- calcualtion outcomes by running 1000
- Compares strategy distributions rather than single results
- Identifies strategy that peroforms well on average and under worst case scenrio

Tyre Strategy modeling:
- Tyre compounds (Soft, Medium, Hard)
- Stint length constraints
- mandartory compound usages rules
- two stop strategy enforce depending on race track that is require

The sample of the code and the GUI displaying for the 78 laps which is monaco and monaco requires 2 pit stop due to high tempt on track. With short track distance requiring 2 stop to continue running til 78 laps comples

<img width="899" height="601" alt="Screenshot 2026-01-06 at 16 22 12" src="https://github.com/user-attachments/assets/10f72234-801f-40f7-880d-288053f4de70" />

<img width="1000" height="300" alt="MonacoTyre" src="https://github.com/user-attachments/assets/7857c64c-8fdc-4ae1-b5e3-bdb45b899820" />

