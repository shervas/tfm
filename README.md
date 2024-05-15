Code used to generate the results presented in Hervas-Raluy, S., Gomez-Benito, M. J., Borau-Zamora, C., Cóndor, M., & Garcia-Aznar, J. M. (2021). A new 3D finite element-based approach for computing cell surface tractions assuming nonlinear conditions. PLoS One, 16(4), e0249018.

https://doi.org/10.1371/journal.pone.0249018

Abstract: Advances in methods for determining the forces exerted by cells while they migrate are essential for attempting to understand important pathological processes, such as cancer or angiogenesis, among others. Precise data from three-dimensional conditions are both difficult to obtain and manipulate. For this purpose, it is critical to develop workflows in which the experiments are closely linked to the subsequent computational postprocessing. The work presented here starts from a traction force microscopy (TFM) experiment carried out on microfluidic chips, and this experiment is automatically joined to an inverse problem solver that allows us to extract the traction forces exerted by the cell from the displacements of fluorescent beads embedded in the extracellular matrix (ECM). Therefore, both the reconstruction of the cell geometry and the recovery of the ECM displacements are used to generate the inputs for the resolution of the inverse problem. The inverse problem is solved iteratively by using the finite element method under the hypothesis of finite deformations and nonlinear material formulation. Finally, after mathematical postprocessing is performed, the traction forces on the surface of the cell in the undeformed configuration are obtained. Therefore, in this work, we demonstrate the robustness of our computational-based methodology by testing it under different conditions in an extreme theoretical load problem and then by applying it to a real case based on experimental results. In summary, we have developed a new procedure that adds value to existing methodologies for solving inverse problems in 3D, mainly by allowing for large deformations and not being restricted to any particular material formulation. In addition, it automatically bridges the gap between experimental images and mechanical computations.