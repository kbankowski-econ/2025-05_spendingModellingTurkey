@#include "declare_all.macro"

@#include "parameters_common.macro"

@#include paramFile

@#include effFile

% gammaa uses the set-specific trend growth rate, so it must come after it
gammaa=g^((1-alpha)/(vartheta-1))-1;

model;

@#include "model_block.modpart"

end;

steady;
check;

shocks;
@#include shockFile
end;

@#include "postSimul.mod"
