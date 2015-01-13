blenderfarm = function(){
    this.m_render_check = null
    
    this.m_render_info_start = {}
    this.m_render_info_stop = {}
    this.m_render_info_resume = {}

    this.render_check = function(){
        clearTimeout(bfobj.m_render_check);
        bfobj.m_render_check = setTimeout(function(){
            bfobj.get_scene_to_render();
            bfobj.render_check();
        }, 3000);
    }

    this.get_scene_to_render = function(){
        send_data = {
            action:'4'
        }; // get scene data
            
        //$('#onprogress-content-start').empty();
        //$('#onprogress-content-stop').empty();
        var html_start = '';
        var html_stop = '';
        
        // filter filename
        var filter_name = $('#find-filename').val().trim();
        
        $.get('parse?send_data=' + btoa(JSON.stringify(send_data)),function(data, status){
            scene_to_render = JSON.parse(atob(data));
            
            // if completed attribute active
            // don't show render start
            if($('#complete-btn').attr('active') != 1){
                if(scene_to_render['render_start'].length){
                
                    render_start = scene_to_render['render_start'];
                    
                    bfobj.m_render_info_start = {}
                    
                    for(var index in render_start){
                    
                        // skip if filter is not found
                        if(render_start[index]['id'].search(filter_name) == -1){
                            continue;
                        }
                        
                        var render_status = 'Not Started';
                        
                        if(parseInt(render_start[index]['render_status'])){
                            render_status = 'Started';
                        }
                        
                        var total_render = (parseInt(render_start[index]['render_uncompleted']) + parseInt(render_start[index]['render_completed']));
                        
                        var stop_btn_id = 'start_' + render_start[index]['id'] + '_' + render_start[index]['name'];
                        var resume_btn_id = 'detail_' + render_start[index]['id'] + '_' + render_start[index]['name'];
                        
                        html_start += '<div class="box-info">'
                            + '<div class="box-info-title">' + render_start[index]['id'] + '.blend</div>'
                                + '<div class="box-info-item">'
                                    + '<div>- Folder Id: ' + render_start[index]['id'] + '</div>'
                                    + '<div>- Total Frame: ' + render_start[index]['frame_end'] + '</div>'
                                    + '<div>- Scene Name: ' + render_start[index]['name'] + '</div>'
                                    + '<div>- Resolution: ' + render_start[index]['resolution_x'] + 'x' + render_start[index]['resolution_y'] + '</div>'
                                    + '<div>- Render Status: ' + render_status + '</div>'
                                    + '<div>- To Render: ' + total_render + '</div>'
                                    + '<div>- Render Completed: ' + render_start[index]['render_completed'] + '</div>'
                                    + '<div>- Render Remaining: ' + render_start[index]['render_uncompleted'] + '</div>'
                                    + '<div style="margin-bottom:5px;border-bottom:solid 1px #8B8E84;"></div>'
                                    + '<div>- Progress: </div>'
                                    + '<div><progress value="' + render_start[index]['render_completed'] + '" max="' + total_render + '"></progress></div>'
                                    + '<div class="box-info-menu">'
                                        + '<div class="render-start-btn-stop" id="' + stop_btn_id + '">Stop Render</div>'
                                    + '</div>'
                                + '</div>'
                            + '</div>';
                            
                        bfobj.m_render_info_start[stop_btn_id] = render_start[index];
                        
                        /*$('#' + stop_btn_id).click(function(render_info){
                            return function(){
                                stop_data = {
                                    action:5, // set_scene_to_render
                                    id:render_info['id'],
                                    name:render_info['name'],
                                    frame:'',
                                    render_status:0,
                                    need_to_render:0,
                                    render_pause:1,
                                };
                                
                                $.get('parse?send_data=' + btoa(JSON.stringify(stop_data)),function(data, status){
                                    if(parseInt(data)){
                                        bfobj.get_scene_to_render();
                                    }
                                });
                            }
                        }(render_start[index]));*/
                    }
                    
                    $('#onprogress-content-start').html(html_start);
                    
                    $('.render-start-btn-stop').each(function(){
                    
                        var id = $(this).attr('id');
                        
                        $('#' + id).click(function(id){
                            return function(){
                            
                                render_info = bfobj.m_render_info_start[id]
                                
                                stop_data = {
                                    action:5, // set_scene_to_render
                                    id:render_info['id'],
                                    name:render_info['name'],
                                    frame:'',
                                    render_status:0,
                                    need_to_render:0,
                                    render_pause:1,
                                };
                                
                                $.get('parse?send_data=' + btoa(JSON.stringify(stop_data)),function(data, status){
                                    //if(parseInt(data)){
                                    //    bfobj.get_scene_to_render();
                                    //}
                                    location.reload();
                                });
                            }
                        }(id));
                    });
                }
            }
            
            if(scene_to_render['render_stop'].length){
            
                render_stop = scene_to_render['render_stop'];
                
                bfobj.m_render_info_stop = {}
                
                for(var index in render_stop){
                
                    if(render_stop[index]['id'].search(filter_name) == -1){
                        continue;
                    }
                        
                    var render_status = 'Not Started';
                    
                    var start = parseInt(render_stop[index]['render_status']);
                    
                    if(start){
                        render_status = 'Started';
                    }
                    
                    var total_render = (parseInt(render_stop[index]['render_uncompleted']) + parseInt(render_stop[index]['render_completed']));
                    
                    if($('#complete-btn').attr('active') == 1
                        && render_stop[index]['render_completed'] == total_render
                        && !total_render){
                        
                        continue;
                    }
                    
                    var start_btn_id = 'start_' + render_stop[index]['id'] + '_' + render_stop[index]['name'];
                    var resume_btn_id = 'resume_' + render_stop[index]['id'] + '_' + render_stop[index]['name'];
                    
                    html_stop += '<div class="box-info">'
                        + '<div class="box-info-title">' + render_stop[index]['id'] + '.blend</div>'
                            + '<div class="box-info-item">'
                                + '<div>- Folder Id: ' + render_stop[index]['id'] + '</div>'
                                + '<div>- Total Frame: ' + render_stop[index]['frame_end'] + '</div>'
                                + '<div>- Scene Name: ' + render_stop[index]['name'] + '</div>'
                                + '<div>- Resolution: ' + render_stop[index]['resolution_x'] + 'x' + render_stop[index]['resolution_y'] + '</div>'
                                + '<div>- Render Status: ' + render_status + '</div>'
                                + '<div>- To Render: ' + total_render + '</div>'
                                + '<div>- Render Completed: ' + render_stop[index]['render_completed'] + '</div>'
                                + '<div>- Render Remaining: ' + render_stop[index]['render_uncompleted'] + '</div>'
                                + '<div style="margin-bottom:5px;border-bottom:solid 1px #8B8E84;"></div>'
                                + '<div>- Progress: </div>'
                                + '<div><progress value="' + render_stop[index]['render_completed'] + '" max="' + total_render + '"></progress></div>'
                                + '<div class="box-info-menu">'
                                    + '<div class="render-stop-btn-start" id="' + start_btn_id + '">Start Render</div>'
                                    + '<div class="render-stop-btn-resume" id="' + resume_btn_id + '">Resume Render</div>'
                                + '</div>'
                            + '</div>'
                        + '</div>';
                    
                    render_stop[index]['btn_start_title'] = 'Start Render';
                    render_stop[index]['btn_resume_hide'] = false;
                    
                    // change button to restart render if render process completed
                    if(total_render == render_stop[index]['render_completed']
                        && total_render){
                        
                        //$('#' + start_btn_id).html("Restart Render");
                        render_stop[index]['btn_start_title'] = 'Restart Render';
                    }
                    
                    // if total render > 0
                    // show resume render button
                    // else hide
                    if(total_render != render_stop[index]['render_completed']
                        && total_render){
                        
                        //$('#' + resume_btn_id).show();
                        //$('#' + start_btn_id).html("Restart Render");
                        render_stop[index]['btn_start_title'] = 'Restart Render';
                        render_stop[index]['btn_resume_hide'] = false;
                    }else{
                        //$('#' + resume_btn_id).hide();
                        render_stop[index]['btn_resume_hide'] = true;
                    }
                    
                    bfobj.m_render_info_stop[start_btn_id] = render_stop[index];
                    bfobj.m_render_info_resume[resume_btn_id] = render_stop[index];
                    
                    /*$('#' + start_btn_id).click(function(render_info){
                        return function(){
                            start_data = {
                                action:5, // set_scene_to_render
                                id:render_info['id'],
                                name:render_info['name'],
                                frame:'',
                                render_status:1,
                                need_to_render:1,
                                render_pause:-1,
                            };
                            
                            $.get('parse?send_data=' + btoa(JSON.stringify(start_data)),function(data, status){
                                if(parseInt(data)){
                                    bfobj.get_scene_to_render();
                                }
                            });
                        }
                    }(render_stop[index]));
                    
                    $('#' + resume_btn_id).click(function(render_info){
                        return function(){
                            start_data = {
                                action:5, // set_scene_to_render
                                id:render_info['id'],
                                name:render_info['name'],
                                frame:'',
                                render_status:1,
                                need_to_render:1,
                                render_pause:0,
                            };
                            
                            $.get('parse?send_data=' + btoa(JSON.stringify(start_data)),function(data, status){
                                if(parseInt(data)){
                                    bfobj.get_scene_to_render();
                                }
                            });
                        }
                    }(render_stop[index]));*/
                }
                
                $('#onprogress-content-stop').html(html_stop);
                
                $('.render-stop-btn-start').each(function(){
                    
                    var id = $(this).attr('id');
                    
                    $('#' + id).html(bfobj.m_render_info_stop[id]['btn_start_title']);
                    
                    $('#' + id).click(function(id){
                        return function(){
                        
                            render_info = bfobj.m_render_info_stop[id]
                            
                            start_data = {
                                action:5, // set_scene_to_render
                                id:render_info['id'],
                                name:render_info['name'],
                                frame:'',
                                render_status:1,
                                need_to_render:1,
                                render_pause:-1,
                            };
                            
                            $.get('parse?send_data=' + btoa(JSON.stringify(start_data)),function(data, status){
                                //if(parseInt(data)){
                                //    bfobj.get_scene_to_render();
                                //}
                                location.reload();
                            });
                        }
                    }(id));
                });
                
                $('.render-stop-btn-resume').each(function(){
                
                    var id = $(this).attr('id');
                    
                    if(bfobj.m_render_info_resume[id]['btn_resume_hide']){
                        $('#' + id).hide();
                    }else{
                        $('#' + id).show();
                    }
                    
                    $('#' + id).click(function(id){
                        return function(){
                        
                            render_info = bfobj.m_render_info_resume[id];
                            
                            start_data = {
                                action:5, // set_scene_to_render
                                id:render_info['id'],
                                name:render_info['name'],
                                frame:'',
                                render_status:1,
                                need_to_render:1,
                                render_pause:0,
                            };
                            
                            $.get('parse?send_data=' + btoa(JSON.stringify(start_data)),function(data, status){
                                //if(parseInt(data)){
                                //    bfobj.get_scene_to_render();
                                //}
                                location.reload();
                            });
                        }
                    }(id));
                });
            }
        });
    }
    
    this.init_script = function(){
        $('#onprogress-btn').click(function(){
            $(this).attr('active', '1');
            $('#complete-btn').attr('active', '0');
            
            $(this).switchClass('menu-header-color', 'menu-header-color-selected');
            $('#complete-btn').switchClass('menu-header-color-selected', 'menu-header-color');
            
            bfobj.get_scene_to_render();
        });
        
        $('#complete-btn').click(function(){
            $(this).attr('active', '1');
            $('#onprogress-btn').attr('active', '0');
            
            $(this).switchClass('menu-header-color', 'menu-header-color-selected');
            $('#onprogress-btn').switchClass('menu-header-color-selected', 'menu-header-color');
            
            bfobj.get_scene_to_render();
        });
        
        $('#find-filename').keyup(function(){
            bfobj.get_scene_to_render();
        });
    }
}

bfobj = new blenderfarm();
