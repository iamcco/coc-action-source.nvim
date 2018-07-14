" call action in async after denite list is hidden
function! cocActionSource#call(...) abort
    let l:cmd = 'call CocAction("' . a:1 . '","' . get(a:, '2', '') . '")'
    call timer_start(100, {-> execute(l:cmd)})
endfunction
