##########################################################################################################
# This file is part of the method that will be soon published in
# If you use any part of it, please cite this paper.
###########################################################################################################
#
#!/usr/bin/env bash
#
# Steps to perform 3D cell traction forces reconstruction:
#
#    The block 1 is used only for the first iteration
#    The block 2 is used for the rest of the iterations
#
#########################################################################################################
#
MEMORY=110000
CPUS=60
CONT=0
CHECK_ERROR=1
MAX_ITER=60
DIEZ=10
#
#########################################################################################################
## Workaround required for conda to work.
source ~/.bashrc
# Activate conda virtual environment.
mkdir -p imago
tar -xjf imago.tar.bz2 -C imago
source imago/bin/activate
conda-unpack
echo "I'm in the venv: " $CONDA_PREFIX

#  BLOCK 0
#
# Initial part: Converts the voxel mesh into a tetrahedral one.
# The displacements must be saved in a file named: displac_known.txt
#
# 0)
#
echo "Hi... we begin the computation"
echo "The value of \"cont\" is $CONT"
# 
mkdir -p calculationFolder/{applyDisp,applyReac,applyReac2}
mkdir -p resultsFolder/it_0/{applyDisp,applyReac,applyReac2}
#
cp ./baseFiles_0/* ./calculationFolder/

cp {apply_displacements_new.inp,displac_known.txt,apply_displacements.inp,displac_known2.txt,apply_displacements4.inp} ./calculationFolder/
cd calculationFolder/
mkdir -p ../resultsFolder/temp
#
cd ..
#
# #########################################################################
while [[ $CHECK_ERROR -eq 1 ]] && [[ $CONT -lt $MAX_ITER ]];
do
echo "The value of \"cont\" is $CONT"
cp ./baseFiles_0/* ./calculationFolder/
cp ./baseFiles_1/* ./calculationFolder/
cd calculationFolder/

mkdir -p ../resultsFolder/"it_${CONT}"/{applyDisp,applyReac,applyReac2}

if [[ $CONT -ne 0 ]]
then
    if ! bash tetra2tetra.sh; then
        echo "error in tetra to tetra"
		cp apply_displacements.inp ../resultsFolder/temp
		cp apply_displacements2.inp ../resultsFolder/temp
		cp apply_displacements3.inp ../resultsFolder/temp
		cp apply_displacements3.ply ../resultsFolder/temp
		cp apply_displacements3.1.ele ../resultsFolder/temp
		cp apply_displacements3.1.node ../resultsFolder/temp
		cp apply_displacements4.inp ../resultsFolder/temp
        cd ..
        tar -czf results.tar.gz resultsFolder
        exit 1
    fi
fi

if [[ $CONT -eq 0 ]]
then
    python3 006_imposedDisplacements_ini.py
else
    python3 006_imposedDisplacements.py
fi

cp apply_displacements_new.inp ./applyDisp/

cd applyDisp
abaqus interactive job=apply_displacements_new.inp memory=$MEMORY cpus=$CPUS

cd ..

abaqus viewer noGUI=Extract_RF_ini.py

python3 imposedReactions_ini.py
python3 Revisar_intro1.py

cp apply_reactions_new.inp ./applyReac/


cp apply_displacements4.inp ./applyReac/
cp Revisar_intro1.py ./applyReac/
cd applyReac
#
abaqus interactive job=apply_reactions_new.inp memory=$MEMORY cpus=$CPUS;

cd ..
abaqus viewer noGUI=Extract_CF.py 
cp reactions_input2.txt ../
cp reactions_input.txt ../
abaqus viewer noGUI=Extract_U.py

if [[ $CONT -eq 0 ]]
then
    python3 postprocData_ini.py
else
    python3 postprocData.py
fi
#
python3 imposedReactions2_ini.py
python3 Revisar_intro2.py
#
cp apply_reactions_2_new.inp ./applyReac2/
cp apply_displacements4.inp ./applyReac2/
cd applyReac2

abaqus interactive job=apply_reactions_2_new.inp memory=$MEMORY cpus=$CPUS;
cd ..
abaqus viewer noGUI=Extract_U2.py


if [[ $CONT -eq 0 ]]
then
    python3 evaluationData_ini.py
else
    python3 evaluationData.py
fi
cp new_displacements_input.txt ../resultsFolder/tempFiles

cp new_displacements_input.txt ../resultsFolder/"it_${CONT}"/
cp apply_displacements.inp ../resultsFolder/"it_${CONT}"/
cp displacements_input2.txt ../resultsFolder/"it_${CONT}"/
cp displac_output_new.txt ../resultsFolder/"it_${CONT}"/
cp reactions_output.txt ../resultsFolder/"it_${CONT}"/
cp reactions_input.txt ../resultsFolder/"it_${CONT}"/
cp error_nodes.txt ../resultsFolder/"it_${CONT}"/
cp max_disp.txt ../resultsFolder/"it_${CONT}"/
cp apply_displacements_new.inp ../resultsFolder/"it_${CONT}"
cp applyDisp/apply_displacements_new.odb ../resultsFolder/"it_${CONT}"/applyDisp
cp applyDisp/apply_displacements_new.inp ../resultsFolder/"it_${CONT}"/applyDisp
cp applyReac/apply_reactions_new.odb ../resultsFolder/"it_${CONT}"/applyReac
cp applyReac/apply_reactions_new.inp ../resultsFolder/"it_${CONT}"/applyReac
cp applyReac2/apply_reactions_2_new.odb ../resultsFolder/"it_${CONT}"/applyReac2
cp applyReac2/apply_reactions_2_new.inp ../resultsFolder/"it_${CONT}"/applyReac2

CHECK_ERROR=$(<check_error.txt)
cd ..

rm -r calculationFolder
mkdir -p calculationFolder/{applyDisp,applyReac,applyReac2}
cp ./resultsFolder/"it_${CONT}"/applyDisp/* ./calculationFolder/
cp ./resultsFolder/"it_${CONT}"/applyReac/* ./calculationFolder/
cp ./resultsFolder/"it_${CONT}"/applyReac2/* ./calculationFolder/
cp ./resultsFolder/"it_${CONT}"/* ./calculationFolder/
#

if [[ $CONT -eq $MAX_ITER ]];
then
    mv ./calculationFolder ./resultsFolder/lastStep
    echo "The base Folder has been moved to the lastStep folder"
fi

CONT=$((CONT+1))
echo "The value of \"cont\" is $CONT"
mkdir -p calculationFolder/{applyDisp,applyReac,applyReac2}
done
##########################################################################################
#
# END OF THE PROGRAM
echo "The program ended with a number of iterations of $CONT"
tar -czf results.tar.gz resultsFolder

source sigopt/bin/deactivate
# DO SOME CLEANUP
rm -rf __pycache__ *.py *.pyc *.tar.bz2

