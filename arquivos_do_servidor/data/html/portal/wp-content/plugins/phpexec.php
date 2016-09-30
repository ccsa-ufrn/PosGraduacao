<?php

/*
Plugin Name: PHP Exec
Plugin URI: http://priyadi.net/archives/2005/03/02/wordpress-php-exec-plugin/
Description: Execute PHP Code inside a post. Do NOT use this plugin if you don't trust your WP users.
Version: 1.7
Author: Priyadi Iman Nurcahyo
Author URI: http://priyadi.net/


Inspired by runphp plugin by Mark Somerville
http://mark.scottishclimbs.com/archives/2004/07/02/running-php-in-wordpress-posts/
*/



### mask code before going to the nasty balanceTags ###
function php_exec_pre($text) {
	$textarr = preg_split("/(<phpcode>.*<\\/phpcode>)/Us", $text, -1, PREG_SPLIT_DELIM_CAPTURE); // capture the tags as well as in between
	$stop = count($textarr);// loop stuff
	for ($phpexec_i = 0; $phpexec_i < $stop; $phpexec_i++) {
		$content = $textarr[$phpexec_i];
		if (preg_match("/^<phpcode>(.*)<\\/phpcode>/Us", $content, $code)) { // If it's a phpcode	
			$content = '[phpcode]' . base64_encode($code[1]) . '[/phpcode]';
		}
		$output .= $content;
	}
	return $output;
}

### unmask code after balanceTags ###
function php_exec_post($text) {
	$textarr = preg_split("/(\\[phpcode\\].*\\[\\/phpcode\\])/Us", $text, -1, PREG_SPLIT_DELIM_CAPTURE); // capture the tags as well as in between
	$stop = count($textarr);// loop stuff
	for ($phpexec_i = 0; $phpexec_i < $stop; $phpexec_i++) {
		$content = $textarr[$phpexec_i];
		if (preg_match("/^\\[phpcode\\](.*)\\[\\/phpcode\\]/Us", $content, $code)) { // If it's a phpcode
			$content = '<phpcode>' . base64_decode($code[1]) . '</phpcode>';
		}
		$output .= $content;
	}
	return $output;
}

### main routine ###
function php_exec_process($phpexec_text) {
	$phpexec_userdata = get_userdatabylogin(the_author('login',false));
	if($phpexec_userdata->user_level >= php_exec_getuserlevel()){
		$phpexec_doeval = true;
	}

	$phpexec_textarr = preg_split("/(<phpcode>.*<\\/phpcode>)/Us", $phpexec_text, -1, PREG_SPLIT_DELIM_CAPTURE); // capture the tags as well as in between
	$phpexec_stop = count($phpexec_textarr);// loop stuff
	for ($phpexec_i = 0; $phpexec_i < $phpexec_stop; $phpexec_i++) {
		$phpexec_content = $phpexec_textarr[$phpexec_i];
		if (preg_match("/^<phpcode>(.*)<\\/phpcode>/Us", $phpexec_content, $phpexec_code)) { // If it's a phpcode	
			$phpexec_php = $phpexec_code[1];
			if ($phpexec_doeval) {
				ob_start();
				eval("?>". $phpexec_php . "<?php ");
				$phpexec_output .= ob_get_clean();
			} else {
				$phpexec_output .= htmlspecialchars($phpexec_php);
			}
		} else {
			$phpexec_output .= $phpexec_content;
		}
	}
	return $phpexec_output;
}

function php_exec_options() {
	if($_POST['php_exec_save']){
		update_option('php_exec_userlevel',$_POST['php_exec_userlevel']);
		echo '<div class="updated"><p>User level saved successfully.</p></div>';
	}

	?>
	<div class="wrap">
	<h2>PHPExec Options</h2>
	<form method="post" id="php_exec_options">
		<fieldset class="options">
		<legend>Minimum User Level</legend>
		<table width="100%" cellspacing="2" cellpadding="5" class="editform"> 
			<tr valign="top"> 
				<th width="33%" scope="row">User Level:</th> 
				<td><input name="php_exec_userlevel" type="text" id="php_exec_userlevel" value="<?php echo get_option('php_exec_userlevel') ;?>" size="2" maxlength="1" />
				<br />Sets the minimum level to allow users to run PHP code in posts. If option is not set, then defaults to 9.</td> 
			</tr>
		</table>
		<p class="submit"><input type="submit" name="php_exec_save" value="Save" /></p>
		</fieldset>
	</form>
	</div>
	<?php
}

function php_exec_adminmenu(){
	add_options_page('PHPExec Options', 'PHPExec', 9, 'phpexec.php', 'php_exec_options');
}

function php_exec_getuserlevel(){
	if($level = get_option('php_exec_userlevel')){
		return $level;
	} else {
		return 9;
	}
}

add_action('admin_menu','php_exec_adminmenu',1);

add_filter('content_save_pre', 'php_exec_pre', 29);
add_filter('content_save_pre', 'php_exec_post', 71);
add_filter('the_content', 'php_exec_process', 2);

add_filter('excerpt_save_pre', 'php_exec_pre', 29);
add_filter('excerpt_save_pre', 'php_exec_post', 71);
add_filter('the_excerpt', 'php_exec_process', 2);

?>
